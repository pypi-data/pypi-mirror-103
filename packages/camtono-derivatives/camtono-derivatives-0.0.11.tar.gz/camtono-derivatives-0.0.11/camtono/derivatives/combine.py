def generate_derivative(definition: dict, feature_map: dict) -> tuple:
    """Create a derived query ast based on a definition and map of all used features

    :param definition: camtono derivative definition
    :param feature_map:
    :return:
    """
    from camtono.derivatives.filters import flatten_filters, generate_filter_query_sets
    # from camtono.derivatives.dependencies import inject_feature_dependencies
    from camtono.parser.clean import prune_ast
    flattened_filters = flatten_filters(filters=definition.get('filters', dict()))
    complete_feature = {
        k: v for k, v in
        feature_map.items()
    }
    default_filters = {i['attribute']: i['value'] for i in definition.get('default_filters', [])}
    default_input = dict(grain=definition['grain'])
    definition_features = {i['feature_id']: i for i in definition.get('features', [])}
    query_sets, filter_features = generate_filter_query_sets(flattened_filters=flattened_filters, features=feature_map,
                                                             default_filters=default_filters,
                                                             default_input=default_input,
                                                             definition_features=definition_features)
    derived_ast = generate_query_skeleton(query_sets=query_sets, grain=definition['grain'], features=complete_feature,
                                          definition_features=definition_features, filter_features=filter_features,
                                          outputs=definition.get('output'))
    return prune_ast(json=derived_ast)


def generate_selects(outputs, grain):
    """
    generate list of selects for query
    if nothing provided in outputs, then using grain
    :param outputs: output field defined inside definition
    :param grain: grain field
    :return:
    """
    output_columns = []
    # without fixed value, keep renaming columns as original column for subquery
    filtered_output_column_map = {}
    if outputs:
        for output in outputs:
            output_dict = {}
            output_dict_without_renaming_or_fixed_value = {}
            if output.get('set_value'):
                output_dict['name'] = output['column_name']
                output_dict['value'] = {"literal": output['set_value']}
            elif output.get('rename_as'):
                output_dict['name'] = output['rename_as']
                output_dict['value'] = output['column_name']
                output_dict_without_renaming_or_fixed_value['value'] = output['column_name']
            else:
                output_dict['value'] = output['column_name']
                output_dict_without_renaming_or_fixed_value = output_dict

            output_columns.append(output_dict)

            if output_dict_without_renaming_or_fixed_value:
                feature_id = output['feature_id'] if output.get('feature_id') else 'common'
                if not filtered_output_column_map.get(feature_id):
                    filtered_output_column_map[feature_id] = []
                filtered_output_column_map[feature_id].append(output_dict_without_renaming_or_fixed_value)
    else:
        output_columns.append({"value": grain})
        filtered_output_column_map['common'] = [{"value": grain}]

    return output_columns, filtered_output_column_map


def generate_query_skeleton(query_sets, grain, features, definition_features, filter_features, outputs):
    base_output_columns, filtered_output_column_map = generate_selects(outputs=outputs, grain=grain)

    base_query = {'with': [], 'from': []}
    union = []
    # TODO handle default input
    for idx, query_set in enumerate(query_sets):
        name, sub_ast, sub_filter_columns = generate_filter_statements(idx=idx, query_set=query_set, grain=grain,
                                                                       output_columns_map=filtered_output_column_map)
        base_query['with'].append({"value": sub_ast, "name": name})
        union.append(
            {"select": sub_filter_columns,  # prefix_selects(output_columns=sub_filter_columns, prefix_str=name + '.'),
             "from": [dict(name=name, value=name)]})
    if union:
        base_query['from'].append(dict(value=dict(union_distinct=union), name='base'))

    feature_selects = []
    for idx, feature in enumerate({k for k in definition_features.keys() if k not in filter_features.keys()}):
        name, sub_ast = generate_feature_statement(idx=idx, feature=features[feature],
                                                   feature_input=definition_features[feature].get('input', []),
                                                   grain=grain)
        feature_specific_columns = filtered_output_column_map.get(feature)
        if feature_specific_columns:
            feature_selects = feature_selects + prefix_selects(output_columns=feature_specific_columns,
                                                               prefix_str=name + '.')
            for column in feature_specific_columns:
                base_output_columns.remove(column)

        if base_query['from']:
            sub_ast = dict(join=sub_ast, using=grain)
        else:
            sub_ast['name'] = 'base'
        base_query['from'].append(sub_ast)

    base_query['select'] = prefix_selects(output_columns=base_output_columns, prefix_str='base.') + feature_selects
    return base_query


def prefix_selects(output_columns, prefix_str):
    from copy import deepcopy
    select_array = []
    if output_columns:
        for column in output_columns:
            if isinstance(column['value'], str):
                updated_column = deepcopy(column)
                updated_column['value'] = prefix_str + column['value']
                select_array.append(updated_column)
            else:
                select_array.append(column)
    return select_array


def generate_filter_statements(idx, query_set, grain, output_columns_map):

    name = "sub_filter_{}".format(idx)
    prefix_str = "f" + str(idx) + "t0."
    select_array = prefix_selects(output_columns=output_columns_map['common'], prefix_str=prefix_str)
    sub_filter_columns = []
    sub_filter_columns = sub_filter_columns + output_columns_map['common']

    sub_ast = {"from": []}
    for query_idx, query in enumerate(query_set):
        # TODO setting join criteria
        table_name = 'f{filter_index}t{query_index}'.format(filter_index=idx, query_index=query_idx)
        from_ = dict(
            value=query['ast'],
            name=table_name
        )
        feature_id = query['feature_id']
        if output_columns_map.get(feature_id):
            select_array = select_array + prefix_selects(output_columns=output_columns_map[feature_id],
                                                         prefix_str=table_name + '.')
            sub_filter_columns = sub_filter_columns + output_columns_map[feature_id]
        if sub_ast['from']:
            sub_ast['from'].append(dict(join=from_, using='{grain}'.format(grain=grain)))
        else:
            sub_ast['from'].append(from_)
    sub_ast['select'] = select_array
    return name, sub_ast, sub_filter_columns


def generate_feature_statement(idx, feature, feature_input, grain):
    from camtono.derivatives.filters import trim_feature_input
    name = 'sub_feature_{}'.format(idx)
    ast = dict(name=name, value=trim_feature_input(
        feature=feature, set_filters=dict(), default_filters=dict(), feature_input=feature_input,
        default_input=dict(grain=grain)
    ))
    return name, ast

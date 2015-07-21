from tessera_client.api.model import (Dashboard,
                                      DashboardDefinition,
                                      DashboardItem,
                                      Row,
                                      Section,
                                      Cell)
import yaml

class TesseraConfiguration(object):
    """
    Simply a wrapper that translates the yml configs into
    models provided by tessera-client module
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.id_generator = self._generate_item_id()


    ## generates IDs for newly created items
    def _generate_item_id(self):
        i = 4
        while True:
            i+=1
            yield "d" + str(i)

    def _generate_definition(self, definition_data):
        queries = self._parse_queries(definition_data['queries'])
        sections = self._parse_sections(definition_data['sections'])

        return DashboardDefinition(queries, items=sections, item_id=self.id_generator.next())

    def generate_dashboard(self):
        config_data = yaml.load(file(self.config_file, "rb"))

        definition = self._generate_definition(config_data['definition'])

        dashboard_context = config_data['metadata']
        dashboard_context['definition_href'] = "/api/dashboard/%s" % dashboard_context['id']
        dashboard_context['href'] = "/api/dashboard/%s" % dashboard_context['id']        
        dashboard_context['definition'] = definition
        dashboard = Dashboard(**dashboard_context)

        return dashboard

    def _parse_queries(self, raw_queries):
        query_result = {}
        for k, v in raw_queries.items():
            if not isinstance(v, list):
                v = [v]
            query_result.update({ k: { 'name': k, 'targets': v } })
        return query_result

    def _parse_sections(self, sections_data):
        section_objs = []
        for section_data in sections_data:
            graphs_data = section_data.pop('graphs')

            # Iterate through graphs. Place 1:1 graph and cell. Place
            # as many graphs into a row as possible (max span 12)
            row_objs = []
            cur_spans = []
            cur_graphs = []
            for graph_data in graphs_data:
                item_type = graph_data.pop('item_type')
                span = graph_data.pop("span")

                if sum(cur_spans) + span > 12:
                    cells = []
                    for graph, span in zip(cur_graphs, cur_spans):
                        cells.append(
                            Cell(span=span,
                                 items=[graph],
                                 item_id=self.id_generator.next()))
                    row_objs.append(Row(items=cells))

                    cur_span = 0
                    cur_graphs = []

                graph_cls = DashboardItem.CLASS_MAP[item_type]
                graph_data['item_id'] = self.id_generator.next()
                cur_graphs.append(graph_cls(**graph_data))
                cur_spans.append(span)

            if cur_graphs:
                cells = []
                for graph, span in zip(cur_graphs, cur_spans):
                    cells.append(
                        Cell(span=span,
                             items=[graph],
                             item_id=self.id_generator.next()))
                row_objs.append(Row(items=cells))

            section_data['items'] = row_objs
            section_data['item_id'] = self.id_generator.next()
            section_objs.append(Section(**section_data))

        return section_objs

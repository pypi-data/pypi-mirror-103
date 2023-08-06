# TODO: cambiar la forma en que se adapta a la version (mucho codigo repetido)

from xml.dom.minidom import parse
import json


class CIMParser():
    """ Parse cim rdf xml files and get the results in json format """

    def __init__(self, eq_file=None, tp_file=None):
        if eq_file is None:
            print("missing files")
            return

        # analize how many files will be parsed
        one_file = False
        if tp_file is None:
            one_file = True
            print("No specified topology file, using one file")

        self.eq_doc = parse(eq_file)
        if not one_file:
            self.tp_doc = parse(tp_file)

        self.json_obj = {}

        # generate all the necessary dicts that will be used to load the information
        self.generate_voltage_dict()
        self.generate_terminal_dict(one_file)
        self.generate_voltage_level_dict()
        self.generate_load_response_dict()
        self.generate_reg_control_dict()
        self.generate_tap_changer_dict()

        # load information to json_obj
        self.add_buses(one_file)
        self.add_lines()
        self.add_generating_units()
        self.add_power_transformers()
        self.add_loads()

    # FUNCTIONS
    def generate_voltage_dict(self):
        """ Create dictionary containing base voltages ids and its voltage value"""

        itemlist = self.eq_doc.getElementsByTagName('cim:BaseVoltage')
        self.voltage_dict = {}  # "baseVoltageID": voltage(kV)

        for item in itemlist:
            self.voltage_dict[item.getAttribute("rdf:ID")] = self.get_data(
                item, "cim:BaseVoltage.nominalVoltage")

    def generate_terminal_dict(self, one_file: bool):
        """ Create dictionary containing a conducting equipment id and which buses
        that equipment is connected to """

        itemlist = self.eq_doc.getElementsByTagName('cim:Terminal')

        self.terminal_dict = {}  # "conductingEquipID": ["bus1ID", "bus2ID"]

        tmp_dict = {}  # "terminalID": "conductingID"

        for item in itemlist:
            conductingID = item.getElementsByTagName("cim:Terminal.ConductingEquipment")[
                0].getAttribute("rdf:resource").replace('#', '')

            if not one_file:
                tmp_dict[item.getAttribute("rdf:ID")] = conductingID
            else:
                if conductingID not in self.terminal_dict:
                    self.terminal_dict[conductingID] = [item.getElementsByTagName(
                        "cim:Terminal.TopologicalNode")[0].getAttribute("rdf:resource").replace('#', '')]
                else:
                    self.terminal_dict[conductingID].append(item.getElementsByTagName(
                        "cim:Terminal.TopologicalNode")[0].getAttribute("rdf:resource").replace('#', ''))

        # if there is topology file, load the terminals from that file
        if not one_file:
            itemlist = self.tp_doc.getElementsByTagName('cim:Terminal')
            for item in itemlist:
                # In topology file the tag used is generally 'rdf:about' instead of 'rdf:ID'
                terminalID = item.getAttribute(
                    "rdf:about").replace('#', '')

                conductingID = tmp_dict[terminalID]
                if conductingID not in self.terminal_dict:
                    self.terminal_dict[conductingID] = [item.getElementsByTagName(
                        "cim:Terminal.TopologicalNode")[0].getAttribute("rdf:resource").replace('#', '')]
                else:
                    self.terminal_dict[conductingID].append(item.getElementsByTagName(
                        "cim:Terminal.TopologicalNode")[0].getAttribute("rdf:resource").replace('#', ''))

    def generate_voltage_level_dict(self):
        """ Create voltage level dictionary containing information like the following example:
            {
                'voltage_level_id': {
                    'name': name,
                    'base_voltage": base_voltage_id,
                    'region': region,
                    'subregion': subregion,
                    'substation': substation
                }
            }
        """

        # "voltage_level_id": voltage_level_info(dict)
        self.voltage_level_dict = {}

        # saving georegions
        # should validate if these fields exist before trying to access

        # saving regions
        itemlist = self.eq_doc.getElementsByTagName('cim:GeographicalRegion')
        regions = {}
        for item in itemlist:
            regions[item.getAttribute("rdf:ID")] = self.get_data(
                item, "cim:IdentifiedObject.name")

        # saving subregions
        subregions = {}
        itemlist = self.eq_doc.getElementsByTagName(
            'cim:SubGeographicalRegion')
        for item in itemlist:
            sID = item.getAttribute("rdf:ID")
            subregions[sID] = {
                "region": item.getElementsByTagName("cim:SubGeographicalRegion.Region")[0].getAttribute('rdf:resource').replace('#', ''),
                "name": self.get_data(item, "cim:IdentifiedObject.name")
            }

        # saving substations
        substations = {}
        itemlist = self.eq_doc.getElementsByTagName('cim:Substation')
        for item in itemlist:
            sID = item.getAttribute("rdf:ID")
            substations[sID] = {
                "subregion": item.getElementsByTagName("cim:Substation.Region")[0].getAttribute('rdf:resource').replace('#', ''),
                "name": self.get_data(item, "cim:IdentifiedObject.name")
            }

        itemlist = self.eq_doc.getElementsByTagName('cim:VoltageLevel')
        for item in itemlist:
            voltage_level = {}
            vID = item.getAttribute("rdf:ID")
            voltage_level['name'] = self.get_data(
                item, "cim:IdentifiedObject.name")
            baseVoltage = item.getElementsByTagName(
                "cim:VoltageLevel.BaseVoltage")
            baseVoltageID = baseVoltage[0].getAttribute(
                "rdf:resource").replace('#', '')
            voltage_level['base_voltage'] = self.voltage_dict[baseVoltageID]

            # Substation
            # support for version 2009 and 2010
            try:
                substationID = item.getElementsByTagName("cim:VoltageLevel.Substation")[
                    0].getAttribute('rdf:resource').replace('#', '')
            except IndexError:
                substationID = item.getElementsByTagName("cim:VoltageLevel.MemberOf_Substation")[
                    0].getAttribute('rdf:resource').replace('#', '')

            subregionID = substations[substationID]['subregion']
            regionID = subregions[subregionID]['region']
            voltage_level['region'] = regions[regionID]
            voltage_level['subregion'] = subregions[subregionID]['name']
            voltage_level['substation'] = substations[substationID]['name']

            self.voltage_level_dict[vID] = voltage_level

    def generate_load_response_dict(self):
        """ Create load response dictionary containing information:
            {
                'response_id': {
                    'exponent_model': true | false,
                    'p_constant_power': value,
                    'q_constant_power': value
                }
            }
        """

        self.load_response_dict = {}  # "response_id": response_info (dict)

        itemlist = self.eq_doc.getElementsByTagName(
            "cim:LoadResponseCharacteristic")
        for item in itemlist:
            response = {}
            respID = item.getAttribute("rdf:ID")
            response['exponent_model'] = self.get_data(
                item, "chighStepm:LoadResponseCharacteristic.exponentModel")
            response['p_constant_power'] = self.get_data(
                item, "cim:LoadResponseCharacteristic.pConstantPower")
            response['q_constant_power'] = self.get_data(
                item, "cim:LoadResponseCharacteristic.qConstantPower")
            self.load_response_dict[respID] = response

    def generate_reg_control_dict(self):
        """ Create regulating control dictionary containing information:
            {
                'reg_control_id': {
                    'name': name,
                    'discrete': true | false,
                    'target_range': value,
                    'target_value': value
                }
            }
            This values are then used to generate the control_v field for
            the synchronous machines
        """

        self.reg_control_dict = {}  # "reg_control_id": reg_control_info(dict)

        itemlist = self.eq_doc.getElementsByTagName("cim:RegulatingControl")
        for item in itemlist:
            reg = {}
            regID = item.getAttribute("rdf:ID")
            reg['name'] = self.get_data(item, "cim:IdentifiedObject.name")
            reg['discrete'] = self.get_data(
                item, "cim:RegulatingControl.discrete")
            reg['target_range'] = self.get_data(
                item, "cim:RegulatingControl.targetRange")
            reg['target_value'] = self.get_data(
                item, "cim:RegulatingControl.targetValue")
            self.reg_control_dict[regID] = reg

    def generate_tap_changer_dict(self):
        """ Create tap changers dictionary containing information:
            {
                'transformer_winding_id': {
                    'high_step': step,
                    'low_Step': step,
                    'neutral_Step': step,
                    'neutralU': U,
                    'step_voltage_increment': value
                }
            }
        """

        self.tap_changer_dict = {}  # "winding_id": tap_changer(dict)

        itemlist = self.eq_doc.getElementsByTagName("cim:RatioTapChanger")
        for item in itemlist:
            tap = {}
            windingID = item.getElementsByTagName("cim:RatioTapChanger.TransformerWinding")[
                0].getAttribute("rdf:resource").replace('#', '')
            tap['high_step'] = self.get_data(item, "cim:TapChanger.highStep")
            tap['low_step'] = self.get_data(item, "cim:TapChanger.lowStep")
            tap['neutral_step'] = self.get_data(
                item, "cim:TapChanger.neutralStep")
            tap['neutralU'] = self.get_data(item, "cim:TapChanger.neutralU")
            tap['step_voltage_increment'] = self.get_data(
                item, "cim:TapChanger.stepVoltageIncrement")

            self.tap_changer_dict[windingID] = tap

    def add_buses(self, one_file: bool):
        """ Add buses to json object. The field 'buses' will be an object with
            the ids of the buses as fields:
            {
                'buses':{
                    'bus1_id':{
                        'name': name,
                        'base_voltage': voltage,
                        'region': region,
                        'subregion': subregion,
                        'substation': substation
                    }
                }
            }
        """

        # If there is a topology file, look for topologicalNode in that file
        if one_file:
            itemlist = self.eq_doc.getElementsByTagName('cim:TopologicalNode')
        else:
            itemlist = self.tp_doc.getElementsByTagName('cim:TopologicalNode')

        buses = {}

        for item in itemlist:
            bus = {}

            busID = item.getAttribute("rdf:ID")
            bus['name'] = self.get_data(item, "cim:IdentifiedObject.name")
            bus['base_voltage'] = self.voltage_dict[item.getElementsByTagName(
                "cim:TopologicalNode.BaseVoltage")[0].getAttribute("rdf:resource").replace('#', '')]

            voltage_levelID = item.getElementsByTagName("cim:TopologicalNode.ConnectivityNodeContainer")[
                0].getAttribute("rdf:resource").replace('#', '')
            try:
                bus['region'] = self.voltage_level_dict[voltage_levelID]['region']
                bus['subregion'] = self.voltage_level_dict[voltage_levelID]['subregion']
                bus['substation'] = self.voltage_level_dict[voltage_levelID]['substation']
            except KeyError as e:
                bus['region'] = "-"
                bus['subregion'] = "-"
                bus['substation'] = "-"

            buses[busID] = bus
        self.json_obj['buses'] = buses

    def add_lines(self):
        # TODO: check if other types of lines exist. (DCLineSegment?)
        """ Add lines to json object. The field 'lines' will be the same as 'buses'
            {
                'lines': {
                    'line1_id': {
                        'name': name,
                        'type': line_type,
                        'base_voltage': voltage,
                        'b0ch': value,
                        'bch': value,
                        'g0ch': value,
                        'gch': value,
                        'length': value,
                        'r': value,
                        'r0': value,
                        'x': value,
                        'x0': value,
                        'buses': [bus1_id, bus2_id]
                    }
                }
            }
        """

        lines = {}
        itemlist = self.eq_doc.getElementsByTagName('cim:ACLineSegment')

        for item in itemlist:
            line = {}

            lineID = item.getAttribute("rdf:ID")
            line["name"] = item.getElementsByTagName(
                "cim:IdentifiedObject.name")[0].firstChild.data
            line["type"] = "ACLineSegment"

            baseVoltage = item.getElementsByTagName(
                "cim:ConductingEquipment.BaseVoltage")
            baseVoltageID = baseVoltage[0].getAttribute(
                "rdf:resource").replace('#', '')
            line['base_voltage'] = self.voltage_dict[baseVoltageID]

            # TODO: change the following one-line ifs to something more friendly

            line["b0ch"] = self.get_data(item, "cim:Conductor.b0ch") if self.get_data(
                item, "cim:ACLineSegment.b0ch") == '-' else self.get_data(item, "cim:ACLineSegment.b0ch")

            line["bch"] = self.get_data(item, "cim:Conductor.bch") if self.get_data(
                item, "cim:ACLineSegment.bch") == '-' else self.get_data(item, "cim:ACLineSegment.bch")

            line["g0ch"] = self.get_data(item, "cim:Conductor.g0ch") if self.get_data(
                item, "cim:ACLineSegment.g0ch") == '-' else self.get_data(item, "cim:ACLineSegment.g0ch")

            line["gch"] = self.get_data(item, "cim:Conductor.gch") if self.get_data(
                item, "cim:ACLineSegment.gch") == '-' else self.get_data(item, "cim:ACLineSegment.gch")

            line["length"] = self.get_data(item, "cim:Conductor.length")
            line["r"] = self.get_data(item, "cim:Conductor.r") if self.get_data(
                item, "cim:ACLineSegment.r") == '-' else self.get_data(item, "cim:ACLineSegment.r")

            line["r0"] = self.get_data(item, "cim:Conductor.r0") if self.get_data(
                item, "cim:ACLineSegment.r0") == '-' else self.get_data(item, "cim:ACLineSegment.r0")

            line["x"] = self.get_data(item, "cim:Conductor.x") if self.get_data(
                item, "cim:ACLineSegment.x") == '-' else self.get_data(item, "cim:ACLineSegment.x")

            line["x0"] = self.get_data(item, "cim:Conductor.x0") if self.get_data(
                item, "cim:ACLineSegment.x0") == '-' else self.get_data(item, "cim:ACLineSegment.x0")

            line['buses'] = self.terminal_dict[lineID]
            lines[lineID] = line

        self.json_obj["lines"] = lines

    def add_generating_units(self):
        """ Add generating units to json object. The field 'generating_units' will have the following structure
            {
                'generating_units': {
                    'gen_unit1_id': {
                        'type': gen_unit_type,
                        'name': name,
                        'governor_SCD': value,
                        'max_operating_P': value,
                        'maximum_allowable_spinning_reserve': value,
                        'min_operating_P': value,
                        'nominal_P': value,
                        'normal_PF': value,
                        'startup_cost': value,
                        'variable_cost': value,
                        'machines': {
                            'machine1_id': {
                                'name': name,
                                'type': type,
                                'maxQ': value,
                                'minQ': value,
                                'qPercent': value,
                                'r': value,
                                'r0': value,
                                'r2': value,
                                'ratedS': value,
                                'x': value,
                                'x0': value,
                                'x2': value,
                                'bus': bus_id,
                                'base_voltage': voltage,
                                'control_v': value,
                            }
                        }
                    }
                }
            }
        """
        units = {}
        # every type of generating unit in the same list
        itemlist = self.eq_doc.getElementsByTagName(
            'cim:GeneratingUnit') + self.eq_doc.getElementsByTagName('cim:WindGeneratingUnit')

        for item in itemlist:
            unit = {}

            unitID = item.getAttribute("rdf:ID")
            unit['type'] = item.localName  # generatingUnit, windGeneratingUnit
            unit['name'] = self.get_data(item, "cim:IdentifiedObject.name")
            unit['governor_SCD'] = self.get_data(
                item, "cim:GeneratingUnit.governorSCD")
            unit['max_operating_P'] = self.get_data(
                item, "cim:GeneratingUnit.maxOperatingP")
            unit['maximum_allowable_spinning_reserve'] = self.get_data(
                item, "cim:GeneratingUnit.maximumAllowableSpinningReserve")
            unit['min_operating_P'] = self.get_data(
                item, "cim:GeneratingUnit.minOperatingP")
            unit['nominal_P'] = self.get_data(
                item, "cim:GeneratingUnit.nominalP")
            unit['normal_PF'] = self.get_data(
                item, "cim:GeneratingUnit.normalPF")
            unit['startup_cost'] = self.get_data(
                item, "cim:GeneratingUnit.startupCost")
            unit['variable_cost'] = self.get_data(
                item, "cim:GeneratingUnit.variableCost")
            unit['machines'] = {}

            units[unitID] = unit

        # Synchronous Machines
        itemlist = self.eq_doc.getElementsByTagName('cim:SynchronousMachine')
        for item in itemlist:
            machine = {}

            machineID = item.getAttribute("rdf:ID")

            machine['name'] = self.get_data(item, "cim:IdentifiedObject.name")
            machine['type'] = "SynchronousMachine"

            # support for version 2009 and 2010
            try:
                parent_gen_unit = item.getElementsByTagName("cim:SynchronousMachine.GeneratingUnit")[
                    0].getAttribute("rdf:resource").replace('#', '')
            except IndexError:
                parent_gen_unit = item.getElementsByTagName("cim:SynchronousMachine.MemberOf_GeneratingUnit")[
                    0].getAttribute("rdf:resource").replace('#', '')

            machine['maxQ'] = self.get_data(
                item, "cim:SynchronousMachine.maxQ")
            machine['minQ'] = self.get_data(
                item, "cim:SynchronousMachine.minQ")
            machine['qPercent'] = self.get_data(
                item, "cim:SynchronousMachine.qPercent")
            machine['r'] = self.get_data(item, "cim:SynchronousMachine.r")
            machine['r0'] = self.get_data(item, "cim:SynchronousMachine.r0")
            machine['r2'] = self.get_data(item, "cim:SynchronousMachine.r2")
            machine['ratedS'] = self.get_data(
                item, "cim:SynchronousMachine.ratedS")
            machine['x'] = self.get_data(item, "cim:SynchronousMachine.x")
            machine['x0'] = self.get_data(item, "cim:SynchronousMachine.x0")
            machine['x2'] = self.get_data(item, "cim:SynchronousMachine.x2")
            machine['bus'] = self.terminal_dict[machineID][0]

            # equip container
            # different names in version 2009 and 2010
            try:
                voltage_levelID = item.getElementsByTagName("cim:ConductingEquipment.BaseVoltage")[
                    0].getAttribute("rdf:resource").replace('#', '')
                machine['base_voltage'] = self.voltage_dict[voltage_levelID]
            except IndexError:
                voltage_levelID = item.getElementsByTagName("cim:Equipment.MemberOf_EquipmentContainer")[
                    0].getAttribute("rdf:resource").replace('#', '')
                machine['base_voltage'] = self.voltage_level_dict[voltage_levelID]['base_voltage']

            # regulating control
            try:
                reg_controlID = item.getElementsByTagName("cim:RegulatingCondEq.RegulatingControl")[
                    0].getAttribute("rdf:resource").replace('#', '')
            except IndexError:
                print(f"No regulating control for machine {machineID}")

            try:
                control_v = float(
                    self.reg_control_dict[reg_controlID]['target_value'])/float(machine['base_voltage'])
            except KeyError as e:
                print(f"No regulating control for machine {machineID}")
                control_v = -1  # meaning we couldn't get the real value
            machine['control_v'] = str(control_v)

            units[parent_gen_unit]['machines'][machineID] = machine

        self.json_obj['generating_units'] = units

    def add_power_transformers(self):
        """ Add power transformers to json object. The field 'power_transoformers' will have the following structure:
            {
                'power_transformers': {
                    'p_transformer_id': {
                        'name': name,
                        'transformer_windings': {
                            'winding_id': {
                                'base_voltage': voltage,
                                'b': value,
                                'b0': value,
                                'g': value,
                                'g0': value,
                                'r': value,
                                'r0': value,
                                'ratedS': value,
                                'ratedU': value,
                                'rground': value,
                                'x': value,
                                'x0': value,
                                'xground': value,
                                'bus': bus_id,
                                'code_connect': value,
                                'type': type,
                                'tap_changer': {
                                    'high_step': step,
                                    'low_Step': step,
                                    'neutral_Step': step,
                                    'neutralU': U,
                                    'step_voltage_increment': value
                                }
                            }
                        }
                    }
                }
            }
        """

        transformers = {}
        itemlist = self.eq_doc.getElementsByTagName('cim:PowerTransformer')

        for item in itemlist:
            transf = {}

            transfID = item.getAttribute("rdf:ID")
            transf['name'] = self.get_data(item, "cim:IdentifiedObject.name")
            transf['transformer_windings'] = {}
            transformers[transfID] = transf

        # Trasnfomer Windings
        itemlist = self.eq_doc.getElementsByTagName('cim:TransformerWinding')

        for item in itemlist:
            winding = {}

            windID = item.getAttribute("rdf:ID")

            baseVoltage = item.getElementsByTagName(
                "cim:ConductingEquipment.BaseVoltage")
            baseVoltageID = baseVoltage[0].getAttribute(
                "rdf:resource").replace('#', '')
            winding['base_voltage'] = self.voltage_dict[baseVoltageID]

            winding['b'] = self.get_data(item, "cim:TransformerWinding.b")
            winding['b0'] = self.get_data(item, "cim:TransformerWinding.b0")
            winding['g'] = self.get_data(item, "cim:TransformerWinding.g")
            winding['g0'] = self.get_data(item, "cim:TransformerWinding.g0")
            winding['r'] = self.get_data(item, "cim:TransformerWinding.r")
            winding['r0'] = self.get_data(item, "cim:TransformerWinding.r0")
            winding['ratedS'] = self.get_data(
                item, "cim:TransformerWinding.ratedS")
            winding['ratedU'] = self.get_data(
                item, "cim:TransformerWinding.ratedU")
            winding['rground'] = self.get_data(
                item, "cim:TransformerWinding.rground")
            winding['x'] = self.get_data(item, "cim:TransformerWinding.x")
            winding['x0'] = self.get_data(item, "cim:TransformerWinding.x0")
            winding['xground'] = self.get_data(
                item, "cim:TransformerWinding.xground")
            winding['bus'] = self.terminal_dict[windID][0]

            # code connect
            con_type_uri = item.getElementsByTagName("cim:TransformerWinding.connectionType")[
                0].getAttribute("rdf:resource")
            con_type = con_type_uri.split("WindingConnection.", 1)[1]
            winding['code_connect'] = con_type

            # winding type
            win_type_uri = item.getElementsByTagName("cim:TransformerWinding.windingType")[
                0].getAttribute("rdf:resource")
            win_type = win_type_uri.split("WindingType.", 1)[1]
            winding['type'] = win_type

            if windID in self.tap_changer_dict:
                winding['tap_changer'] = self.tap_changer_dict[windID]
            else:
                winding['tap_changer'] = {}

            # different names in versions 2009 and 2010
            try:
                parent_transf = item.getElementsByTagName("cim:TransformerWinding.PowerTransformer")[
                    0].getAttribute("rdf:resource").replace('#', '')
            except IndexError:
                parent_transf = item.getElementsByTagName("cim:TransformerWinding.MemberOf_PowerTransformer")[
                    0].getAttribute("rdf:resource").replace('#', '')

            transformers[parent_transf]['transformer_windings'][windID] = winding

        self.json_obj['power_transformers'] = transformers

    def add_loads(self):
        """ Add loads (energy consumers) to json object
            {
                'loads': {
                    load_id: {
                        'name': name,
                        'bus': bus_id,
                        'load_response': {
                            'exponent_model': true | false,
                            'p_constant_power': value,
                            'q_constant_power': value
                        }
                        'base_voltage': voltage,
                        'region': region,
                        'subregion': subregion,
                        'substation': substation
                    }
                }
            }
        """

        loads = {}
        itemlist = self.eq_doc.getElementsByTagName('cim:EnergyConsumer')

        for item in itemlist:
            load = {}
            consumerID = item.getAttribute("rdf:ID")
            load['name'] = self.get_data(item, "cim:IdentifiedObject.name")
            load['bus'] = self.terminal_dict[consumerID][0]
            responseID = item.getElementsByTagName("cim:EnergyConsumer.LoadResponse")[
                0].getAttribute('rdf:resource').replace('#', '')
            load['load_response'] = self.load_response_dict[responseID]
            voltage_levelID = item.getElementsByTagName("cim:Equipment.MemberOf_EquipmentContainer")[
                0].getAttribute('rdf:resource').replace('#', '')
            load['base_voltage'] = self.voltage_level_dict[voltage_levelID]['base_voltage']
            load['region'] = self.voltage_level_dict[voltage_levelID]['region']
            load['subregion'] = self.voltage_level_dict[voltage_levelID]['subregion']
            load['substation'] = self.voltage_level_dict[voltage_levelID]['substation']

            loads[consumerID] = load

        self.json_obj['loads'] = loads

    def get_data(self, item, tag):
        """ Get tag value for an xml object """
        arr = item.getElementsByTagName(tag)
        if arr == []:
            return "-"
        return arr[0].firstChild.data

    def get_json(self):
        """ Returns json formatted output """
        return json.dumps(self.json_obj, indent=4)

    def get_dict(self):
        """ Returns python dictionary formatted output """
        return self.json_obj

    def save_json(self, file_name):
        """ Save json to a given file path """
        with open(file_name, 'w') as f:
            json.dump(self.json_obj, f, indent=4)

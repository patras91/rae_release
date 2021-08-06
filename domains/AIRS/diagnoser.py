__author__ = 'patras'
from domains.constants import *
from enum import IntEnum

class CONFIDENCE(IntEnum):
    LOW = 0.1
    MEDIUM = 0.5
    HIGH = 0.8

class AIRSDiagnoser():
    def __init__(self, state, rv, actor, env, domain):

        self.state = state
        self.actor = actor
        self.env = env
        self.rv = rv
        self.domain = domain

        self.actor.declare_task('__diagnose')

        self.actor.declare_methods(
                '__diagnose',
                self.m1_diagnose,
            )

        self.state.diagnosed_attack = {0: None}

        self.confidence = {}
        for item in self.Attacks.__dict__:
            self.confidence[item] = CONFIDENCE.LOW

        self.confidence_threshold = CONFIDENCE.HIGH

    class Attacks():
        Switch_Identification_Spoofing = "Switch_Identification_Spoofing"
        Switch_Table_Flooding = "Switch_Table_Flooding"
        Malformed_OpenFlow_Version_Number = "Malformed_OpenFlow_Version_Number"
        Corrupted_Control_Message_Type = "Corrupted_Control_Message_Type"
        Control_Message_Drop = "Control_Message_Drop"
        Control_Message_Infinite_Loop = "Control_Message_Infinite_Loop"
        Flow_Rule_Modification = "Flow_Rule_Modification"
        PACKET_IN_Flooding = "PACKET_IN_Flooding"
        Flow_Rule_Flooding = "Flow_Rule_Flooding"
        Switch_Firmware_Misuse = "Switch_Firmware_Misuse"
        Flow_Table_Clearance = "Flow_Table_Clearance"
        Southbound_Interface_Eavesdropping = "Southbound_Interface_Eavesdropping"
        Southbound_Interface_Man_in_the_Middle = "Southbound_Interface_Man_in_the_Middle"
        Unflagged_Flow_Remove_Notification = "Unflagged_Flow_Remove_Notification"
        Internal_Storage_Misuse = "Internal_Storage_Misuse"
        Application_Eviction = "Application_Eviction"
        Event_Listener_Unsubscription = "Event_Listener_Unsubscription"
        System_Command_Execution = "System_Command_Execution"
        Memory_Exhaustion = "Memory_Exhaustion"
        CPU_Exhaustion = "CPU_Exhaustion"
        System_Variable_Manipulation = "System_Variable_Manipulation"
        East_West_Bound_Channel_Attack = "East_West_Bound_Channel_Attack"
        Service_Unregistration_Attack = "Service_Unregistration_Attack"
        Link_Discovery_Neutralization_Attack = "Link_Discovery_Neutralization_Attack"
        Northbound_Interface_Eavesdropping = "Northbound_Interface_Eavesdropping"
        Side_Channel_Attack = "Side_Channel_Attack"
        Host_ID_Spoofing = "Host_ID_Spoofing"
        Policy_Conflict_Threat = "Policy_Conflict_Threat"
        Management_Console_Attack = "Management_Console_Attack"
        Link_Fabrication = "Link_Fabrication"



    def m1_diagnose(self):
        while(True):
            for atk in self.Attacks.__dict__:
                if self.confidence[atk] == self.confidence_threshold:
                    self.state.diagnosed_attack = {0: atk}
                    return

            self.diagnose_scenario1()

    def diagnose_scenario1(self):
        self.actor.do_command(self.domain.getSwitchRespFromController)
        self.actor.do_command(self.domain.getNonRespSwitches)

        #TODO: remove the following line because it will be computed the SM
        self.state.nonResponsiveSwitches = {0: ['s1','s2', 's3']}


        if len(self.state.nonResponsiveSwitches[0]) > 0:
            for s in self.state.nonResponsiveSwitches[0]:
                self.actor.do_command(self.domain.probeSwitchHeartBeats, s)

                #TODO: remove the following line because it will be computed the SM
                self.state.switchHeartBeat = {'s1':10, 's2':30, 's3':None}

                if not self.state.switchHeartBeat[s]:
                    self.diagnose_scenario7()
                    return

        self.actor.do_command(self.domain.getCPUFromSwitch)

        # TODO: remove the following
        self.confidence[self.Attacks.Switch_Table_Flooding] = CONFIDENCE.HIGH


    def diagnose_scenario7(self):
        pass


if __name__=="__main__":
    for item in AIRSDiagnoser.Attacks.__dict__:
        if not item[0] == "_":
            print(item)



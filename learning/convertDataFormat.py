import torch
import math
import ast
import numpy as np
import pdb
folderPrefix = "../../raeResults/AIJ2020/learning/"
from paramInfo import *

import sys
sys.path.append("encoders/")

def ConvertToOneHotHelper(label, upper):
	onehot = np.zeros(upper)
	onehot[int(label)] = 1
	return list(onehot)

def ConvertToOneHot(a_int, varName, domain):
	nRange_SV = { # size of the range of state variables, used in the one hot encoding
	"CR": {
		"loc": 11,
		"charge": 5,
		"load": 4,
		"pos": 13,
		"emergencyHandling": 2,
		"view": 2,
	},
	"SR": {
		"loc": 30, #31
		"medicine": 6,
		"weather": 4,
		"status": 9,
		"currentImage": 2, #31
		"altitude": 2,
		"robot": 3,
	},
	"SD": {
		"loc": 8,
		"pos": 12,
		"status": 3,
		"doorType": 4,
		"doorStatus": 4,
		"load": 5,
	}, 
	"EE": {
		"loc": 8,
		"charge": 11, # 11 unit blocks 0 to 100
		"data": 5, # 0 to 4
		"pos": 11, # 8 locations + 3 robots
		"load": 8, # 5 equipments + 1 charger + nil
	},
	"OF": {
		"OBJECTS": 2,
		"OBJ_WEIGHT": 15,
		"OBJ_CLASS": 5,
		"loc": 15,
		"busy": 2,
		"nObjects": 12,
		'nPallets': 3,
		'nMachines': 5,
	}
	}

	aH = []
	for i in a_int:
		aH += ConvertToOneHotHelper(i, nRange_SV[domain][varName])
	return aH

from encoder_CR import *
from encoder_SR import *
from encoder_SD import *
from encoder_EE import *
from encoder_OF import *

def GetLabel(yhat):
    r, predicted = torch.max(yhat, 0)
    return predicted.long()

intervals = {
	# CR 100
	# SD 75
	# SR 10
	#"CR": [0, 1.925559114336333e-05, 3.947396184389483e-05, 6.07032510794529e-05, 8.299400477678888e-05, 0.00010639929615899165, 0.00013097485211030458, 0.00015677918585918314, 0.00018387373629550564, 0.00021232301425364426, 0.00024219475610968983, 0.00027356008505853764, 0.00030649368045482787, 0.0003410739556209326, 0.00037738324454534254, 0.000415507997915973, 0.00045553898895513503, 0.0004975715295462551, 0.0005417056971669311, 0.0005880465731686411, 0.0006367044929704365, 0.0006877953087623216, 0.0007414406653438011, 0.0007977682897543545, 0.0008569122953854357, 0.0009190135012980708, 0.0009842197675063377, 0.001052686347025018, 0.0011245762555196323, 0.0012000606594389774, 0.0012793192835542895, 0.0013625408388753674, 0.0014499234719624991, 0.0015416752367039875, 0.0016380145896825503, 0.0017391709103100413, 0.0018453850469689068, 0.0019569098904607157, 0.0020740109761271147, 0.002196967116076834, 0.0023260710630240394, 0.002461630207318605, 0.0026039673088278986, 0.002753421265412657, 0.0029103479198266534, 0.0030751209069613495, 0.0032481325434527805, 0.003429794761768783, 0.0036205400910005853, 0.003820822686693978, 0.00403111941217204, 0.004251930973924006, 0.00448378311376357, 0.004727227860595111, 0.00498284484476823, 0.0052512426781500055, 0.00553306040320087, 0.005828969014504277, 0.006139673056372854, 0.00646591230033486, 0.0068084635064949665, 0.007168142272963078, 0.007545804977754596, 0.007942350817785689, 0.008358723949818337, 0.008795915738452618, 0.009254967116518614, 0.009736971063487908, 0.010243075207805668, 0.010774484559339315, 0.011332464378449645, 0.011918343188515491, 0.01253351593908463, 0.013179447327182224, 0.0138576752846847, 0.014569814640062299, 0.015317560963208778, 0.01610269460251258, 0.01692708492378157, 0.017792694761114013, 0.01870158509031308, 0.0196559199359721, 0.02065797152391407, 0.021710125691253135, 0.022814887566959156, 0.023974887536450478, 0.025192887504416367, 0.02647178747078055, 0.027814632435462942, 0.029224619648379455, 0.03070510622194179, 0.032259617124182245, 0.03389185357153472, 0.03560570184125482, 0.037405242524460924, 0.039294760241827334, 0.04127875384506206, 0.04336194712845853, 0.045549300076024826, 0.047846020670969436, 1],
	"CR": [0, 3.991874036777851e-05, 8.183341775394595e-05, 0.00012584382900942176, 0.00017205476082767136, 0.00022057623923683347, 0.0002715237915664537, 0.0003250187215125549, 0.0003811883979559612, 0.00044016655822153776, 0.0005020936265003931, 0.0005671170481931913, 0.0006353916409706295, 0.0007070799633869394, 0.0007823527019240649, 0.0008613890773880468, 0.0009443772716252277, 0.0010315148755742677, 0.0011230093597207596, 0.001219078568074576, 0.0013199512368460835, 0.0014258675390561662, 0.001537079656376753, 0.0016538523795633694, 0.0017764637389093164, 0.0019052056662225607, 0.0020403846899014672, 0.002182322664764319, 0.0023313575383703137, 0.0024878441556566077, 0.002652155103807217, 0.0028246815993653563, 0.0030058344197014027, 0.0031960448810542516, 0.003395765865474743, 0.0036054728991162586, 0.0038256652844398504, 0.004056867289029622, 0.004299629393848882, 0.004554529603909104, 0.004822174824472338, 0.005103202306063734, 0.005398281161734699, 0.005708113960189213, 0.006033438398566452, 0.006375029058862554, 0.00673369925217346, 0.007110302955149912, 0.0075057368432751865, 0.007920942425806725, 0.00835690828746484, 0.008814672442205861, 0.009295324804683933, 0.009800009785285908, 0.010329929014917982, 0.01088634420603166, 0.011470580156701021, 0.012084027904903852, 0.012728148040516824, 0.013404474182910445, 0.014114616632423747, 0.014860266204412713, 0.01564319825500113, 0.016465276908118963, 0.01732845949389269, 0.018234801208955105, 0.019186460009770638, 0.02018570175062695, 0.021234905578526076, 0.02233656959782016, 0.023493316818078945, 0.02470790139935067, 0.025983215209685984, 0.027322294710538063, 0.028728328186432745, 0.03020466333612216, 0.03175481524329605, 0.03338247474582863, 0.03509151722348784, 0.03688601182503001, 0.03877023115664929, 0.04074866145484954, 0.042826013267959796, 0.045007232671725565, 0.047297513045679626, 0.049702307438331386, 0.05222734155061574, 0.05487862736851431, 0.05766247747730781, 0.06058552009154098, 0.06365471483648581, 0.06687736931867788, 0.07026115652497955, 0.07381413309159632, 0.07754475848654392, 0.0814619151512389, 0.08557492964916863, 0.08989359487199484, 0.09442819335596236, 0.09918952176412826, 1],
	"SR": [0, 0.00015524707093654436, 0.000426929445075497, 0.0009023735998186641, 0.0017344008706192066, 0.0031904485945201556, 0.0057385321113468165, 0.010197678265793472, 0.018001184036075122, 0.03165731913406801, 1],
	"SD": [0, 3.489955672036314e-06, 7.398706024716986e-06, 1.1776506419719338e-05, 1.6679642862121975e-05, 2.217115567761293e-05, 2.8321650030962798e-05, 3.5210203706714654e-05, 4.292538382355673e-05, 5.156638555441986e-05, 6.124430749298656e-05, 7.208358006418127e-05, 8.422356534391934e-05, 9.782034885722598e-05, 0.00011304874639212942, 0.00013010455163122128, 0.00014920705349900416, 0.000170601855590921, 0.00019456403393386783, 0.0002214016736779683, 0.00025145983019136085, 0.0002851249654863605, 0.0003228299170167601, 0.0003650594627308077, 0.000412356553930541, 0.0004653292960742423, 0.0005246587672751877, 0.0005911077750202466, 0.0006655306636947125, 0.0007488842990101144, 0.0008422403705633646, 0.0009467991707030047, 0.0010639050268594016, 0.0011950635857545663, 0.0013419611717171507, 0.0015064864679952452, 0.0016907547998267112, 0.001897135331477953, 0.002128281526927344, 0.0023871652658306614, 0.0026771150534023774, 0.003001858815482699, 0.0033655718290126597, 0.0037729304041662155, 0.004229172008338198, 0.004740162605010818, 0.005312472073284153, 0.005953458677750289, 0.00667136367475236, 0.007475417271394681, 0.00837595729963408, 0.009384562131262207, 0.010514199542685709, 0.011779393443480031, 0.013196410612369673, 0.014783469841526072, 0.01656097617818124, 0.018551783275235025, 0.020781487223935267, 0.023278755646479538, 0.02607569627972912, 0.029208269788968653, 0.03271675211931693, 0.036646252329307, 0.04104729256449588, 0.045976457627907426, 0.051497122498928356, 0.057680267154471804, 0.06460538916868046, 0.07236152582459415, 0.0810483988792175, 0.09077769670039565, 0.10167451026011518, 0.11387894144700104, 0.12754790437631322, 1],
	#"EE": [0, 0.00012771268983702522, 0.00026181101416590166, 0.000402614254711222, 0.0005504576572838083, 0.0007056932299850239, 0.0008686905813213004, 0.0010398378002243907, 0.0012195423800726356, 0.0014082321889132927, 0.0016063564881959825, 0.001814387002442807, 0.0020328190424019725, 0.0022621726843590965, 0.002502994008414077, 0.002755856398671806, 0.0030213619084424217, 0.0033001426937015682, 0.003592862518223672, 0.003900218333971881, 0.0042229419405075, 0.0045618017273699, 0.004917604503575421, 0.005291197418591217, 0.005683469979357803, 0.006095356168162719, 0.00652783666640788, 0.006981941189565299, 0.00745875093888059, 0.007959401175661645, 0.008485083924281753, 0.009037050810332866, 0.009616616040686535, 0.010225159532557888, 0.010864130199022808, 0.011535049398810974, 0.012239514558588549, 0.012979202976355003, 0.01375587581500978, 0.014571382295597294, 0.015427664100214185, 0.01632675999506192, 0.017270810684652044, 0.018262063908721673, 0.01930287979399478, 0.020395736473531545, 0.021543235987045148, 0.022748110476234432, 0.02401322868988318, 0.025341602814214364, 0.026736395644762108, 0.02820092811683724, 0.02973868721251613, 0.03135333426297896, 0.033048713665964936, 0.03482886203910021, 0.03669801783089225, 0.03866063141227389, 0.04072137567272461, 0.042885157146197866, 0.04515712769334479, 0.04754269676784906, 0.050047544296078536, 0.05267763420071949, 0.05543922860059249, 0.05833890272045914, 0.061383560546319126, 0.06458045126347212, 0.06793718651648276, 0.07146175853214393, 0.07516255914858815, 0.07904839979585458, 0.08312853247548434, 0.08741267178909558, 0.09191101806838739, 0.09663428166164378, 0.101593708434563, 0.10680110654612818, 0.11226887456327161, 0.11801003098127222, 0.12403824522017286, 0.13036787017101853, 0.1370139763694065, 0.14399238787771385, 0.15131971996143656, 0.15901341864934543, 0.16709180227164974, 0.17557410507506926, 0.18448052301865975, 0.19383226185942976, 0.20365158764223829, 0.21396187971418723, 0.22478768638973362, 0.23615478339905735, 0.24809023525884724, 0.2606224597116266, 0.273781295387045, 0.2875980728462343, 0.30210568917838304, 0.31733868632713924, 1],
	"EE": [0, 9.638602071624609e-07, 1.975913424683045e-06, 3.0385693030796577e-06, 4.1543579753961015e-06, 5.325936081328368e-06, 6.5560930925572474e-06, 7.847757954347572e-06, 9.204006059227412e-06, 1.0628066569351243e-05, 1.2123330104981267e-05, 1.369335681739279e-05, 1.534188486542489e-05, 1.7072839315858596e-05, 1.889034148881399e-05, 2.079871877041715e-05, 2.280251491610047e-05, 2.4906500869067957e-05, 2.7115686119683818e-05, 2.943533063283047e-05, 3.1870957371634455e-05, 3.442836544737864e-05, 3.711364392691003e-05, 3.9933186330418e-05, 4.289370585410136e-05, 4.600225135396889e-05, 4.92662241288298e-05, 5.269339554243375e-05, 5.62919255267179e-05, 6.007038201021626e-05, 6.403776131788953e-05, 6.820350959094648e-05, 7.257754527765626e-05, 7.717028274870154e-05, 8.199265709329908e-05, 8.705615015512649e-05, 9.237281787004528e-05, 9.795531897071001e-05, 0.00010381694512640797, 0.00010997165258989084, 0.00011643409542654785, 0.00012321966040503772, 0.00013034450363245208, 0.00013782558902123714, 0.00014568072867946147, 0.00015392862532059701, 0.00016258891679378935, 0.00017168222284064127, 0.0001812301941898358, 0.00019125556410649007, 0.00020178220251897705, 0.00021283517285208836, 0.00022444079170185524, 0.00023662669149411046, 0.00024942188627597844, 0.00026285684079693984, 0.0002769635430439493, 0.0002917755804033092, 0.00030732821963063713, 0.00032365849081933146, 0.0003408052755674605, 0.000358809399552996, 0.00037771372973780833, 0.0003975632764318612, 0.00041840530046061673, 0.00044028942569081003, 0.00046326775718251304, 0.0004873950052488012, 0.0005127286157184037, 0.0005393289067114864, 0.0005672592122542233, 0.0005965860330740969, 0.0006273791949349643, 0.000659712014888875, 0.0006936614758404812, 0.0007293084098396678, 0.0007667376905388136, 0.0008060384352729168, 0.0008473042172437252, 0.000890633288313074, 0.0009361288129358902, 0.0009838991137898472, 0.0010340579296865022, 0.0010867246863779897, 0.0011420247809040517, 0.0012000898801564168, 0.0012610582343714001, 0.0013250750062971327, 0.0013922926168191518, 0.001462871107867272, 0.001536978523467798, 0.0016147913098483505, 0.0016964947355479305, 0.0017822833325324896, 0.0018723613593662767, 0.001966943287541753, 0.0020662543121260034, 0.0021705308879394663, 0.002280021292543602, 0.0023949862173779446, 0.0025156993884540044, 0.0026424482180838673, 0.002775534489195223, 0.0029152750738621466, 0.0030620026877624163, 0.0032160666823577, 0.0033778338766827475, 0.0035476894307240473, 0.0037260377624674123, 0.0039133035107979455, 0.004109932546545006, 0.004316393034079418, 0.004533176545990551, 0.004760799233497241, 0.004999803055379266, 0.005250757068355392, 0.0055142587819803236, 0.005790935581286502, 0.00608144622055799, 0.006386482391793053, 0.006706770371589868, 0.007043072750376524, 0.007396190248102513, 0.007766963620714802, 0.008156275661957705, 0.008565053305262754, 0.008994269830733054, 0.00944494718247687, 0.009918158401807877, 0.010415030182105434, 0.010936745551417867, 0.011484546689195924, 0.012059737883862883, 0.01266368863826319, 0.013297836930383512, 0.01396369263710985, 0.014662841129172507, 0.015396947045838296, 0.016167758258337373, 0.016977110031461407, 0.01782692939324164, 0.018719239723110886, 0.019656165569473593, 0.020639937708154435, 0.02167289845376932, 0.02275750723666495, 0.023896346458705364, 0.025092127641847796, 0.02634769788414735, 0.02766604663856188, 0.029050312830697138, 0.030503792332439158, 0.03202994580926828, 0.03363240695993886, 0.03531499116814297, 0.03708170458675728, 0.03893675367630231, 0.04088455522032459, 0.04292974684154798, 0.04507719804383255, 0.04733202180623134, 0.04969958675675007, 0.05218552995479474, 0.05479577031274164, 0.05753652268858588, 0.060414312683222345, 0.06343599217759063, 0.06660875564667733, 0.06994015728921836, 0.07343812901388644, 0.07711099932478793, 0.08096751315123449, 0.08501685266900338, 0.08926865916266072, 0.09373305598100092, 0.09842067264025813, 0.10334267013247819, 0.10851076749930927, 0.1139372697344819, 0.11963509708141316, 0.12561781579569098, 0.1318996704456827, 0.13849561782817402, 0.14542136257978988, 0.15269339456898653, 0.16032902815764302, 0.16834644342573235, 0.17676472945722613, 0.1856039297902946, 0.1948850901400165, 0.2046303085072245, 0.2148627877927929, 0.2256068910426397, 0.23688819945497885, 0.24873357328793497, 0.2611712158125389, 0.274230740463373, 0.2879432413467488, 0.30234136727429345, 0.3174593994982153, 1],

}
methodCodes = {
	"CR": {
	'Search_Method1': 0, 
	'Search_Method2': 1,
	'Fetch_Method1': 2, 
	'Fetch_Method2': 3,
	'Recharge_Method1': 4, 
	'Recharge_Method2': 5,
	'Recharge_Method3': 6,
	'MoveTo_Method1': 7,
 	'Emergency_Method1': 8,
	'NonEmergencyMove_Method1': 9,
	},
	"SR": {
    'MoveTo_Method4' : 0,
    'MoveTo_Method3': 1, 
    'MoveTo_Method2': 2, 
    'MoveTo_Method1': 3,
    'Rescue_Method1': 4,
    'Rescue_Method2': 5,
    'HelpPerson_Method2': 6,
    'HelpPerson_Method1': 7, 
    'GetSupplies_Method2': 8,
    'GetSupplies_Method1': 9,
    'Survey_Method1': 10,
    'Survey_Method2': 11,
    'GetRobot_Method1': 12,
    'GetRobot_Method2': 13,
    'AdjustAltitude_Method1': 14,
    'AdjustAltitude_Method2': 15,
	},
	"SD": {
	"Fetch_Method1": 0,
	"MoveTo_Method1": 1,
	"MoveThroughDoorway_Method1": 2,
	"MoveThroughDoorway_Method3": 3,
	"MoveThroughDoorway_Method4": 4,
	"MoveThroughDoorway_Method2": 5,
	"Unlatch_Method1": 6,
	"Unlatch_Method2": 7,
	"Recover_Method1": 8,
	},
	"EE": {
	"Explore_Method1": 0,
    "GetEquipment_Method1": 1,
    "GetEquipment_Method2": 2,
    "GetEquipment_Method3": 3,
    "MoveTo_Method1": 4,
    "FlyTo_Method1": 5,
    "FlyTo_Method2": 6,
    "Recharge_Method1": 7,
    "Recharge_Method2": 8,
    "DepositData_Method1": 9,
    "DepositData_Method2": 10, 
    "DoActivities_Method1": 11, 
    "DoActivities_Method2": 12, 
    "DoActivities_Method3": 13,
    "HandleEmergency_Method2": 14, 
    "HandleEmergency_Method1": 15,
    "HandleEmergency_Method3": 16,
	},
	"OF": {
	"OrderStart_Method1": 0,
	"Order_Method1": 1,
	"Order_Method2": 2,
	"PickupAndLoad_Method1": 3,
	"UnloadAndDeliver_Method1": 4,
	"MoveToPallet_Method1": 5,
	"Redoer": 6,
	}
}

numMethods = {
	"CR": 10,
	"SR": 16,
	"EE": 17,	
	"SD": 9,
	"OF": 7,
}

numTasks = {
	'CR': 7,
	'SR': 8,
	'SD': 6,
	'EE': 9,
	'OF': 6,
}

taskCodes = {
	"CR": {
	'search': 1,
	'fetch': 2,
	'recharge': 3,
	'moveTo': 4,
	'emergency': 5,
	'nonEmergencyMove': 6
	},
	"SR": {
	'moveTo': 1,
	'rescue': 2,
	'helpPerson': 3,
	'getSupplies': 4,
	'survey': 5,
	'getRobot': 6,
	'adjustAltitude': 7,
	},
	"SD": {
	"fetch": 1,
	"moveTo": 2,
	"moveThroughDoorway": 3,
	"unlatch": 4,
	"collision": 5,
	},
	"EE": {
	'explore': 1,
	'getEquipment': 2,
	'flyTo': 3,
	'moveTo': 4,
	'recharge': 5,
	'depositData': 6, 
	'doActivities': 7,
	'handleEmergency': 8,
	},
	"OF": {
	'orderStart ': 1,
	'order': 2,
	'pickupAndLoad': 3,
	'unloadAndDeliver': 4,
	'moveToPallet': 5,
	'redoer': 6,
	}
}

domain = None

def AddToRecordsAllTogether_LearnH(l, new):
	if len(l) % 100 == 0:
		print(len(l))
	for i in range(len(l)):
		item = l[i]
		if new[0:-1] == item[0:-1]:
			n = AddToRecordsAllTogether_LearnH.Counts[i]
			eff = (float(new[-1]) + n * float(item[-1]))/(n+1)
			item[-1] = str(eff)
			#print("Updated ", i)
			AddToRecordsAllTogether_LearnH.Counts[i] += 1
			return
	l.append(new)
	AddToRecordsAllTogether_LearnH.Counts.append(1)
AddToRecordsAllTogether_LearnH.Counts = []

def AddToRecordsAllTogether_LearnM(l, new):
	if len(l) % 100 == 0:
		print(len(l))
	if new not in l: 
		l.append(new)

def AddToRecords_MethodParamBased_LearnMI(domain, l, r1, m, methodLine): # m is the name of the method
	instantiatedParams = {
			"SD": GetOneHotInstantiatedParamValue_SD,
			"OF": GetOneHotInstantiatedParamValue_OF,
		}[domain](methodLine, m)

	for p in params[domain][m]:
		r2 = r1 + instantiatedParams + {
			"SD": GetIntParamValue_SD,
			"OF": GetIntParamValue_OF,
		}[domain](p, methodLine, m)
		
		if r2 not in l[m][p]:
			l[m][p].append(r2)
			#print(r2)

import argparse

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]

def Encode_LearnM(domain, state, task, mainTask):
	return {
		"CR": EncodeState_CR,
		"SD": EncodeState_SD,
		"SR": EncodeState_SR,
		"EE": EncodeState_EE,
		"OF": EncodeState_OF,
	}[domain](state) + ConvertToOneHotHelper(taskCodes[domain][task], numTasks[domain])

def Encode_LearnH(domain, state, method, taskAndArgs):
	p1 = {
		"CR": EncodeState_CR,
		"SD": EncodeState_SD,
		"SR": EncodeState_SR,
		"EE": EncodeState_EE,
		"OF": EncodeState_OF,
	}[domain](state)

	if domain != "CR":
		p1 += {
			"SD": ReadTaskAndArgs_SD,
			"SR": ReadTaskAndArgs_SR,
			"EE": ReadTaskAndArgs_EE,
			"OF": ReadTaskAndArgs_OF,
		}[domain](taskAndArgs)

	p1 += ConvertToOneHotHelper(methodCodes[domain][method], numMethods[domain])
	return p1

def Encode_LearnMI(domain, state, method, taskAndArgs):
	p1 = {
		"SD": EncodeState_SD,
		"OF": EncodeState_OF,
	}[domain](state)

	mLine = method + ' ' + ' '.join(taskAndArgs.split(' ')[1:])

	if domain == "SD":
		p1 += ReadOnlyTaskArgs_SD(taskAndArgs)
		p1 += GetOneHotInstantiatedParamValue_SD(mLine, method)
	elif domain == "OF":
		p1 += ReadOnlyTaskArgs_OF(taskAndArgs)
		p1 += GetOneHotInstantiatedParamValue_OF(mLine, method)

	return p1

def Decode_LearnMI(domain, method, p, yhat):
	label = GetLabel(yhat)
	return params[domain][method][p]['decoder'](int(label))

def Decode_LearnH(domain, interval):
	num = GetLabel(interval)
	return (intervals[domain][num] + intervals[domain][num + 1])/2

	#num = GetLabel(interval)
	#return (num +0.5)*0.0010419 

def Decode_LearnM(domain, yhat):
	label = GetLabel(yhat)
	for m in methodCodes[domain]:
		if methodCodes[domain][m] == label:
			return m
	return None

def normalize(l):
	l2 = []
	for item in l:
		res = []
		for x in item:
			p = x.split(' ')
			for y in p:
				res.append(float(y))
		l2.append(res)

	n = len(l2)
	sums = [0]*len(l2[0])
	for item in l2:
		for i in range(len(item)):
			sums[i] += item[i]

	means = [x/n for x in sums]

	var = [0]*len(l2[0])
	for item in l2:
		for i in range(len(item)):
			var[i] += (item[i] - means[i])*(item[i] - means[i])/(n-1)

	sigmas = [math.sqrt(x) for x in var]

	#print(l2)
	print(sigmas[-1])
	print(means[-1])

	for item in l2:
		for i in range(len(item)):
			if sigmas[i] != 0:
				item[i] = (item[i] - means[i])/sigmas[i]

	return l2

def DivideIntoIntervalsEqual(l):
	maxE = 0
	for item in l:
		e = float(item[-1])
		if e > maxE:
			maxE = e

	step = maxE/100

	print("step = ", step, " maxE = ", maxE)

	for item in l:
		e = float(item[-1])
		i = math.floor(e/step)
		item[-1] = str(i)
	return l

def DivideIntoIntervals(l, domain):
	eMax = 0
	for item in l:
		e = float(item[-1])
		if e > eMax:
			eMax = e

	numIntervals = {
		"CR": 100,
		"SR": 10,
		"SD": 75,
		"EE": 200,
	}

	factor = {
		"CR": 1.05,
		"SR": 1.75,
		"SD": 1.12,
		"EE": 1.05,
	}

	widths = []
	sum = 0
	for i in range(numIntervals[domain]):
		x = pow(factor[domain], i) 
		widths.append(x)
		sum += x

	intervalLimits = [0]*numIntervals[domain]

	num = 0
	for i in range(numIntervals[domain]):
		intervalLimits[i] = num
		widths[i] *= eMax/sum
		num += widths[i]

	print(intervalLimits)

	for item in l:
		e = float(item[-1])
		item[-1] = numIntervals[domain] - 1
		for i in range(numIntervals[domain]):
			if e < intervalLimits[i]:
				item[-1] = str(i-1)
				break
	return l

def ReadTaskAndArgs_LearnH(taskAndArgs, domain):
	if domain == "CR":
		return []
	else:
		return {
			"SR": ReadTaskAndArgs_SR,
			"SD": ReadTaskAndArgs_SD,
			"EE": ReadTaskAndArgs_EE,
			"OF": ReadTaskAndArgs_OF,
		}[domain](taskAndArgs)

def ReadOnlyTaskArgs_LearnMI(taskAndArgs, domain):
	return {
		"SD": ReadOnlyTaskArgs_SD,
		"OF": ReadOnlyTaskArgs_OF,
	}[domain](taskAndArgs)

if __name__ == "__main__":

	argparser = argparse.ArgumentParser()
	argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', EE', 'OF']",
                           type=str, required=True)
	argparser.add_argument("--dataFrom", help="actor (a) or planner (p) ?",
                           type=str, required=True)
	argparser.add_argument("--learnWhat", help="learnM, learnMI or learnH",
						   type=str, required=True)
	argparser.add_argument("--howMany", help="how many training data records to read?",
						   type=int, required=True)
	args = argparser.parse_args()
	
	domain, learnWhat = args.domain, args.learnWhat
	
	assert(learnWhat == 'learnM' or learnWhat == "learnH" or learnWhat == "learnMI")
	assert(args.dataFrom == 'a' or args.dataFrom=="p")
	suffix = 'actor' if args.dataFrom == 'a' else 'planner'

	if learnWhat == "learnM":
		fname = folderPrefix + "{}/{}_data_{}.txt".format(domain, domain, suffix)
		fwrite = open(folderPrefix + "{}/numericData_{}_{}.txt".format(domain, domain, suffix), "w")
		recordL = []

	elif learnWhat == "learnH":
		if domain != "CR":
			fname = folderPrefix + "{}/{}_data_eff_{}_without_dup.txt".format(domain, domain, suffix)
		else:
			fname = folderPrefix + "{}/{}_data_eff_{}.txt".format(domain, domain, suffix)
		fwrite = open(folderPrefix + "{}/numericData_eff_{}_{}.txt".format(domain, domain, suffix), "w")
		recordL = []

	elif learnWhat == "learnMI":
		fname = folderPrefix + "{}/{}_data_{}_mi_without_dups.txt".format(domain, domain, suffix)
		fwrite = {}
		recordL = {}
		for method in params[domain]:
			fwrite[method] = {}
			recordL[method] = {}
			for p in params[domain][method]:
				recordL[method][p] = []
				fwrite[method][p] = open(folderPrefix + "{}/numericData_mi_{}_{}_{}_{}.txt".format(domain, domain, suffix, method, p), "w")

	f = open(fname)
	
	line = f.readline()
	while(line != ""):
		record = {
			"CR": ReadStateVars_CR,
			"SD": ReadStateVars_SD,
			"SR": ReadStateVars_SR,
			"EE": ReadStateVars_EE,
			"OF": ReadStateVars_OF,
		}[domain](line, f)

		taskAndArgs = f.readline()[0:-1]
		mainTask = f.readline()[0:-1]
		method = f.readline()[0:-1].split(' ')[0]

		#taskCode = taskCodes[domain][taskAndArgs]
		
		eff = f.readline()[0:-1]

		if learnWhat == "learnM":
			mainTaskCode = taskCodes[domain][mainTask]
			#record.append(str(mainTaskCode))
			params = taskAndArgs.split(' ')
			
			taskCode = taskCodes[domain][params[0]]
			taskCode = ConvertToOneHotHelper(taskCode, numTasks[domain])
			taskCode = [str(i) for i in taskCode]
			record += taskCode

			record.append(str(methodCodes[domain][method]))

		elif learnWhat == "learnH":
			mainTaskCode = taskCodes[domain][mainTask]
			record += ReadTaskAndArgs_LearnH(taskAndArgs, domain)
			
			methodCode = methodCodes[domain][method]
			methodCode = ConvertToOneHotHelper(methodCode, numMethods[domain])
			methodCode = [str(i) for i in methodCode]
			record += methodCode

			if eff == "inf":
				eff = 1
			record.append(str(eff))

		else: # learnWhat == "learnMI"
			record += ReadOnlyTaskArgs_LearnMI(taskAndArgs, domain)
			methodParts = method.split(' ')
			methodName = methodParts[0]

		if learnWhat == "learnH":
			AddToRecordsAllTogether_LearnH(recordL, record)
		elif learnWhat == "learnM":
			AddToRecordsAllTogether_LearnM(recordL, record)
		elif learnWhat == "learnMI":
			AddToRecords_MethodParamBased_LearnMI(domain, recordL, record, methodName, method)

		if len(recordL) % 100 == 0:
			print(len(recordL))
		if len(recordL) > args.howMany:
			break

		line = f.readline()
	f.close()

	if learnWhat == "learnH":
		record_LearnH = DivideIntoIntervals(recordL, domain)
		for item in record_LearnH:
			fwrite.write(" ".join([str(i) for i in item]) + "\n")
		print(len(record_LearnH[0]))

	elif learnWhat == "learnM":
		for item in recordL:
			fwrite.write(" ".join(item) + "\n")
		print(len(recordL[0]))

	elif learnWhat == "learnMI":
		for methodName in params[domain]:
			for p in params[domain][methodName]:
				print(methodName, p, len(recordL[methodName][p][0]))
				for item in recordL[methodName][p]:
					fwrite[methodName][p].write(" ".join([str(i) for i in item]) + "\n")


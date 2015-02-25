from cv2 import *
from naoqi import *
import cv2
import numpy as np
import Image
import LeftKick
import time

NAMES_LEFT = list()
TIMES_LEFT = list()
KEYS_LEFT = list()

NAMES_LEFT.append("HeadPitch")
TIMES_LEFT.append([ 0.58000, 1.34000, 1.60000, 2.12000, 2.56000, 3.46000])
KEYS_LEFT.append([ [ 0.04363, [ 3, -0.19333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.26180, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.17453, [ 3, -0.08667, 0.06012], [ 3, 0.17333, -0.12023]], [ -0.27925, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.26180, [ 3, -0.14667, -0.00403], [ 3, 0.30000, 0.00825]], [ -0.24241, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("HeadYaw")
TIMES_LEFT.append([ 0.58000, 1.34000, 1.60000, 2.12000, 2.56000, 3.46000])
KEYS_LEFT.append([ [ -0.00464, [ 3, -0.19333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.00149, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.00311, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.04905, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.03371, [ 3, -0.14667, 0.00268], [ 3, 0.30000, -0.00548]], [ 0.02459, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LAnklePitch")
TIMES_LEFT.append([ 0.52000, 0.66000, 0.88000, 1.12000, 1.28000, 1.42000, 1.54000, 1.68000, 1.84000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ 0.08727, [ 3, -0.17333, 0.00000], [ 3, 0.04667, 0.00000]], [ -0.08727, [ 3, -0.04667, 0.08824], [ 3, 0.07333, -0.13866]], [ -0.59341, [ 3, -0.07333, 0.00000], [ 3, 0.08000, 0.00000]], [ -0.40143, [ 3, -0.08000, -0.14312], [ 3, 0.05333, 0.09541]], [ 0.12217, [ 3, -0.05333, 0.00000], [ 3, 0.04667, 0.00000]], [ -0.05236, [ 3, -0.04667, 0.04386], [ 3, 0.04000, -0.03759]], [ -0.12217, [ 3, -0.04000, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.24435, [ 3, -0.04667, 0.00000], [ 3, 0.05333, 0.00000]], [ -0.12217, [ 3, -0.05333, 0.12468], [ 3, 0.07333, -0.17144]], [ -0.64403, [ 3, -0.07333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.21991, [ 3, -0.14667, -0.07049], [ 3, 0.30000, 0.14419]], [ 0.00000, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LAnkleRoll")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ -0.40143, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.10887, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.13802, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.00000, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.18097, [ 3, -0.12667, 0.05338], [ 3, 0.14667, -0.06181]], [ -0.34558, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.05066, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LElbowRoll")
TIMES_LEFT.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
KEYS_LEFT.append([ [ -0.64117, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ -1.15353, [ 3, -0.25333, 0.18364], [ 3, 0.08667, -0.06282]], [ -1.38056, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ -1.36062, [ 3, -0.17333, -0.01994], [ 3, 0.14667, 0.01687]], [ -0.96024, [ 3, -0.14667, -0.09905], [ 3, 0.30000, 0.20261]], [ -0.45564, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LElbowYaw")
TIMES_LEFT.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
KEYS_LEFT.append([ [ -0.99714, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.86368, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.90970, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.63205, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.84834, [ 3, -0.14667, 0.09469], [ 3, 0.30000, -0.19368]], [ -1.49714, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LHand")
TIMES_LEFT.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
KEYS_LEFT.append([ [ 0.00129, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.00136, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.00132, [ 3, -0.08667, 0.00001], [ 3, 0.17333, -0.00002]], [ 0.00128, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.00133, [ 3, -0.14667, -0.00005], [ 3, 0.30000, 0.00010]], [ 0.00391, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LHipPitch")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ 0.16265, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.39726, [ 3, -0.25333, 0.31826], [ 3, 0.08667, -0.10888]], [ -1.11876, [ 3, -0.08667, 0.00190], [ 3, 0.04667, -0.00102]], [ -1.11978, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.78540, [ 3, -0.12667, -0.12796], [ 3, 0.14667, 0.14816]], [ -0.29142, [ 3, -0.14667, -0.10930], [ 3, 0.30000, 0.22356]], [ 0.21318, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LHipRoll")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ 0.47124, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.54001, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.32218, [ 3, -0.08667, 0.09040], [ 3, 0.04667, -0.04868]], [ 0.12276, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 0.36360, [ 3, -0.12667, -0.04547], [ 3, 0.14667, 0.05265]], [ 0.41713, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 0.05825, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LKneePitch")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.42000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ -0.08901, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.97575, [ 3, -0.25333, 0.00000], [ 3, 0.04667, 0.00000]], [ 1.97222, [ 3, -0.04667, 0.00353], [ 3, 0.04000, -0.00302]], [ 1.23918, [ 3, -0.04000, 0.26583], [ 3, 0.04667, -0.31013]], [ 0.24435, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 1.53589, [ 3, -0.12667, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.62430, [ 3, -0.14667, 0.17650], [ 3, 0.30000, -0.36102]], [ -0.07666, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LShoulderPitch")
TIMES_LEFT.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
KEYS_LEFT.append([ [ 1.52782, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.46033, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 1.47413, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.24096, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 1.51862, [ 3, -0.14667, -0.01504], [ 3, 0.30000, 0.03076]], [ 1.54938, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LShoulderRoll")
TIMES_LEFT.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
KEYS_LEFT.append([ [ 0.12268, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.04138, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.14569, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.13955, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.14722, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 0.03993, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("LWristYaw")
TIMES_LEFT.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
KEYS_LEFT.append([ [ 0.08727, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.07359, [ 3, -0.25333, 0.00911], [ 3, 0.08667, -0.00312]], [ 0.05058, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.06285, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.05680, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.00149, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RAnklePitch")
TIMES_LEFT.append([ 0.52000, 0.88000, 1.28000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ 0.03226, [ 3, -0.17333, 0.00000], [ 3, 0.12000, 0.00000]], [ 0.01745, [ 3, -0.12000, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.01745, [ 3, -0.13333, 0.00000], [ 3, 0.26000, 0.00000]], [ 0.03491, [ 3, -0.26000, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.03491, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.00117, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RAnkleRoll")
TIMES_LEFT.append([ 0.52000, 0.88000, 1.28000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ -0.33161, [ 3, -0.17333, 0.00000], [ 3, 0.12000, 0.00000]], [ -0.36652, [ 3, -0.12000, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.36652, [ 3, -0.13333, 0.00000], [ 3, 0.26000, 0.00000]], [ -0.36652, [ 3, -0.26000, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.34732, [ 3, -0.14667, -0.01920], [ 3, 0.30000, 0.03927]], [ 0.08433, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RElbowRoll")
TIMES_LEFT.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
KEYS_LEFT.append([ [ 0.74096, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.03396, [ 3, -0.25333, -0.15621], [ 3, 0.08667, 0.05344]], [ 1.36990, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.02015, [ 3, -0.17333, 0.11965], [ 3, 0.14667, -0.10124]], [ 0.70722, [ 3, -0.14667, 0.07036], [ 3, 0.30000, -0.14392]], [ 0.37732, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RElbowYaw")
TIMES_LEFT.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
KEYS_LEFT.append([ [ 1.15353, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.95411, [ 3, -0.25333, 0.06096], [ 3, 0.08667, -0.02085]], [ 0.90809, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.23023, [ 3, -0.17333, -0.11716], [ 3, 0.14667, 0.09913]], [ 1.55697, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 1.14441, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RHand")
TIMES_LEFT.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
KEYS_LEFT.append([ [ 0.00317, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.00328, [ 3, -0.25333, -0.00003], [ 3, 0.08667, 0.00001]], [ 0.00329, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.00317, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.00325, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 0.00187, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RHipPitch")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ 0.23159, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.10580, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.12217, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.08433, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 0.09046, [ 3, -0.12667, -0.00614], [ 3, 0.14667, 0.00710]], [ 0.19171, [ 3, -0.14667, -0.00904], [ 3, 0.30000, 0.01849]], [ 0.21020, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RHipRoll")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ 0.34366, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.36820, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.36820, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.36513, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 0.36667, [ 3, -0.12667, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.36513, [ 3, -0.14667, 0.00153], [ 3, 0.30000, -0.00314]], [ -0.10129, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RHipYawPitch")
TIMES_LEFT.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ -0.18097, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.25307, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.06285, [ 3, -0.08667, -0.02279], [ 3, 0.04667, 0.01227]], [ -0.05058, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.18711, [ 3, -0.12667, 0.02986], [ 3, 0.14667, -0.03457]], [ -0.24386, [ 3, -0.14667, 0.01444], [ 3, 0.30000, -0.02954]], [ -0.31903, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RKneePitch")
TIMES_LEFT.append([ 0.52000, 0.88000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
KEYS_LEFT.append([ [ -0.08727, [ 3, -0.17333, 0.00000], [ 3, 0.12000, 0.00000]], [ -0.08727, [ 3, -0.12000, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.09235, [ 3, -0.13333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.07973, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ -0.07973, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.07819, [ 3, -0.12667, -0.00047], [ 3, 0.14667, 0.00055]], [ -0.07666, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.09208, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RShoulderPitch")
TIMES_LEFT.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
KEYS_LEFT.append([ [ 1.48649, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.35917, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 1.41746, [ 3, -0.08667, -0.02659], [ 3, 0.17333, 0.05318]], [ 1.59847, [ 3, -0.17333, -0.03988], [ 3, 0.14667, 0.03375]], [ 1.63835, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 1.50021, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RShoulderRoll")
TIMES_LEFT.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
KEYS_LEFT.append([ [ -0.02305, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.01998, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.13197, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.11816, [ 3, -0.17333, -0.01381], [ 3, 0.14667, 0.01168]], [ -0.02305, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.03524, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

NAMES_LEFT.append("RWristYaw")
TIMES_LEFT.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
KEYS_LEFT.append([ [ -0.24435, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.23935, [ 3, -0.25333, -0.00500], [ 3, 0.08667, 0.00171]], [ -0.22094, [ 3, -0.08667, -0.00409], [ 3, 0.17333, 0.00818]], [ -0.20253, [ 3, -0.17333, -0.00554], [ 3, 0.14667, 0.00469]], [ -0.19026, [ 3, -0.14667, -0.01227], [ 3, 0.30000, 0.02510]], [ 0.12736, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

names = list()
times = list()
keys = list()


    
names.append("LHipYawPitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.00456, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.01538, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LHipRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.13810, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.13964, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LHipPitch")
times.append([ 2.60000, 5.00000, 5.20000])
keys.append([ [ -0.28528, [ 3, -0.86667, 0.00000], [ 3, 0.80000, 0.00000]], [ -0.56549, [ 3, -0.80000, 0.10950], [ 3, 0.06667, -0.00913]], [ -0.64117, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LKneePitch")
times.append([ 2.60000, 5.00000, 5.20000])
keys.append([ [ 1.02007, [ 3, -0.86667, 0.00000], [ 3, 0.80000, 0.00000]], [ 1.91812, [ 3, -0.80000, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.97558, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LAnklePitch")
times.append([ 2.60000, 5.00000, 5.20000])
keys.append([ [ -0.69955, [ 3, -0.86667, 0.00000], [ 3, 0.80000, 0.00000]], [ -0.46251, [ 3, -0.80000, -0.17606], [ 3, 0.06667, 0.01467]], [ -0.12736, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("LAnkleRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.00311, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.00311, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RHipRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.11202, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.11202, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RHipPitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.20253, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ -0.20406, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RKneePitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ 0.83761, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ 0.84528, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RAnklePitch")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.45862, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ -0.46016, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

names.append("RAnkleRoll")
times.append([ 2.60000, 5.20000])
keys.append([ [ -0.23466, [ 3, -0.86667, 0.00000], [ 3, 0.86667, 0.00000]], [ -0.23466, [ 3, -0.86667, 0.00000], [ 3, 0.00000, 0.00000]]])

# This is the range that the ball needs to be within such that we consider it
# centered on the screen. If the ball is within this range, the robot should
# move forward. So if the camera is 100x100 then the at x=50, the range of the
# center would be from x=35 to x=65. Obviously this value will need some tweaking
# and slowly get smaller as the robot moves towards the ball.
CENTER_RANGE = 0.2
LEFT_FOOT_RANGE = 0.2

CAMERA_WIDTH = 0
CAMERA_HEIGHT = 0

# Where the ball is on the screen.
LEFT_SIDE = -1
CENTER = 0
RIGHT_SIDE = 1
LEFT_FOOT_ALIGNED = 2
UNKNOWN = None
BALL_LOCATION = None
LAST_LOCATION = None

NEAR_FEET = False

color_tracker_window = "Track Red Ball Now"

# NAO
motionProxy = None
camProxy = None
videoClient = None

TURN_RIGHT = -0.15
TURN_LEFT = 0.15
MOVE_FORWARD_FAST = .2
MOVE_FORWARD_KICK = .07
MOVE_FORWARD_SLOW = .05
MOVE_BACKWARD = -.1
MOVE_FORWARD = MOVE_FORWARD_FAST
# NAO HEAD
HEAD_DOWN = .78
HEAD_FORWARD = .25
CURRENT_HEAD = HEAD_FORWARD

# States
state = 0
MOVING_TO_BALL = 0
PREPARING_KICK = 1


IP = "169.254.183.153"
PORT = 9559

def setHeadAngle(headAngle):
    CURRENT_HEAD = headAngle
    n  = ["HeadPitch"]
    angles  = [headAngle]
    fractionMaxSpeed  = 0.2
    motionProxy.setAngles(n, angles, fractionMaxSpeed)

def goalieKick():
    print 'Moving to Ball!'
    state = MOVING_TO_BALL

    while state == MOVING_TO_BALL:
        ball_tracker.run()
        if (NEAR_FEET):
            if (BALL_LOCATION == LEFT_SIDE):
                motionProxy.moveTo(0, 0, TURN_LEFT)
            if (BALL_LOCATION == RIGHT_SIDE):
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            if (BALL_LOCATION == CENTER):
                motionProxy.moveTo(-.05, 0, 0)
                state = PREPARING_KICK
                tts.say("Any last words?. Naughty ball?")
                print 'Preparing Kick!'
        elif (BALL_LOCATION == UNKNOWN):
            if (LAST_LOCATION == LEFT_SIDE):
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            if (LAST_LOCATION == RIGHT_SIDE):
                motionProxy.moveTo(0, 0, TURN_LEFT)
            if (LAST_LOCATION == CENTER):
                motionProxy.moveTo(-.05, 0, 0)

        elif (BALL_LOCATION == LEFT_SIDE):
            motionProxy.moveTo(0, 0, TURN_LEFT)
            print 'Turn Right'
        elif (BALL_LOCATION == RIGHT_SIDE):
            motionProxy.moveTo(0, 0, TURN_RIGHT)
            print 'Turn Left'
        elif (BALL_LOCATION == CENTER):
            motionProxy.moveTo(MOVE_FORWARD, 0, 0)
            print 'Walk Forward'

            if cv.WaitKey(10) == 27:
                break

    while state == PREPARING_KICK:
        ball_tracker.run()
        if (BALL_LOCATION == CENTER): #Normnally BALL_LOCATION == LEFT_LEG_ALIGNED
            print 'Power Up Kick!'
            motionProxy.moveTo(MOVE_FORWARD_KICK, 0, 0)
            tts.say("Commence ball kicking!")
            time.sleep(2)
            motionProxy.angleInterpolationBezier(names, times, keys)
            break
        elif (BALL_LOCATION == LEFT_SIDE):
            print '1'
            motionProxy.moveTo(0, 0, TURN_LEFT)
        elif (BALL_LOCATION == RIGHT_SIDE or BALL_LOCATION == CENTER):
            print '2'
            motionProxy.moveTo(0, 0, TURN_RIGHT)
        elif (BALL_LOCATION == UNKNOWN):
            if (LAST_LOCATION == LEFT_SIDE):
                print '3'
                motionProxy.moveTo(0, 0, TURN_LEFT)
            elif (LAST_LOCATION == RIGHT_SIDE):
                print '4'
                motionProxy.moveTo(0, 0, TURN_RIGHT)
            else:
                print '5'
                motionProxy.moveTo(-.05, 0, 0)

        if cv.WaitKey(10) == 27:
            break

class BallTracker:

    def __init__(self):
        cv.NamedWindow(color_tracker_window, 1)
        # self.capture = cv.CaptureFromCAM(1)

    def run(self):
        global BALL_LOCATION, LAST_LOCATION, MOVE_FORWARD, CURRENT_HEAD, NEAR_FEET, CENTER_RANGE

        img = camProxy.getImageRemote(videoClient)
        im = Image.fromstring("RGB", (img[0], img[1]), img[6])
        
        CAMERA_WIDTH, CAMERA_HEIGHT = im.size

        center_x_start = (CAMERA_WIDTH / 2) - \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)
        center_x_end = (CAMERA_WIDTH / 2) + \
            int((CAMERA_WIDTH * CENTER_RANGE) / 2)

        left_foot_start = 60
        left_foot_end   = 60+(CAMERA_WIDTH * LEFT_FOOT_RANGE)

        frame = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(frame, im.tostring(), im.size[0] * 3)
        # cv.SaveImage("bb.png", frame)

        img = frame
        cv.CvtColor(img, img, cv.CV_RGB2BGR)
        # blur theself source image to reduce color noise
        cv.Smooth(img, img, cv.CV_BLUR, 3)

        # convert the image to hsv(Hue, Saturation, Value) so its
        # easier to determine the color to track(hue)
        hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

        thresholded_img = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)

        # Finds a red ball color! DO NOT DELETE THIS IT TOOK FOREVER TO GET THE RIGHT COLOR STUPID
        # OPENCV AND ITS BS WAY OF DOING HSV... /rant COMMENT OUT IF
        # NEEDED. :)
        cv.InRangeS(hsv_img, cv.Scalar(170, 100, 100), cv.Scalar(
            180, 255, 255), thresholded_img)

        # determine the objects moments and check that the area is large
        # enough to be our object
        moments = cv.Moments(cv.GetMat(thresholded_img), 0)
        area = cv.GetCentralMoment(moments, 0, 0)

        # there can be noise in the video so ignore objects with small areas
        # if(area > 100000):
        if(area > 10000):
            # determine the x and y coordinates of the center of the object
            # we are tracking by dividing the 1, 0 and 0, 1 moments by the
            # area
            x = int(cv.GetSpatialMoment(moments, 1, 0) / area)
            y = int(cv.GetSpatialMoment(moments, 0, 1) / area)

            # create an overlay to mark the center of the tracked object
            #overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
            
            # shows the white dot on the object.
            # cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20)
            # cv.Add(img, overlay, img)

            if(x < center_x_start):
                BALL_LOCATION = LEFT_SIDE
                LAST_LOCATION = LEFT_SIDE
            elif(x > center_x_end):
                BALL_LOCATION = RIGHT_SIDE
                LAST_LOCATION = RIGHT_SIDE
            else:
                BALL_LOCATION = CENTER
                LAST_LOCATION = CENTER

            if(CURRENT_HEAD == HEAD_DOWN):
                if(y > (CAMERA_HEIGHT/2)):
                    print '---Ball is near feet!---'
                    CENTER_RANGE = .1
                    NEAR_FEET = True

            if(y > (CAMERA_HEIGHT - (CAMERA_HEIGHT/3))):
                print '----HEAD NOW DOWN----'
                CURRENT_HEAD = HEAD_DOWN
                MOVE_FORWARD = MOVE_FORWARD_SLOW
                setHeadAngle(HEAD_DOWN)
            #else:
            #    print '----HEAD NOW FORWARD----'
            #    setHeadAngle(HEAD_FORWARD)
            #    MOVE_FORWARD = MOVE_FORWARD_FAST

            #print 'x: ', x, ' left end:', left_foot_end
            #if((x < left_foot_end and x > left_foot_start) and state == PREPARING_KICK):
            #    print 'LEFT_FOOT_ALIGNED'
            #    BALL_LOCATION = LEFT_FOOT_ALIGNED



        else:
            BALL_LOCATION = UNKNOWN

        cv.ShowImage(color_tracker_window, img)

if __name__ == "__main__":
    camProxy        = ALProxy("ALVideoDevice", IP, PORT)
    motionProxy     = ALProxy("ALMotion", IP, PORT)
    postureProxy    = ALProxy("ALRobotPosture", IP, PORT)
    tts             = ALProxy("ALTextToSpeech", IP, PORT) 
    tts.setParameter("doubleVoice", 1)
    tts.setParameter("doubleVoiceLevel", 1)

    videoClient = camProxy.subscribe("pyclient3", 1, 11, 5)
    camProxy.setParam(18, 1)

    # We will need a loop here that calls ball_tracker.run(), then calls a method
    # to make the robot do movements based on the BALL_LOCATION results of ball_tracker.run()
    # BALL_LOCATION
    ball_tracker = BallTracker()

    #Stand the robot up
    postureProxy.goToPosture("StandInit", 0.5)

    # Move to the ball, then back up slightly
    tts.say("Stand back citizen! A ball needs to be kicked!")
    # Example showing how to set angles, using a fraction of max speed
    
    setHeadAngle(HEAD_FORWARD)
    goalieKick()

    postureProxy.goToPosture("Sit", 0.5)

    camProxy.unsubscribe(videoClient)
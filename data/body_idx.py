class BodyIdx:
    def __init__(self):
        self.L_ASIS = self._3(1)
        self.R_ASIS = self._3(4)
        self.L_PSIS = self._3(7)
        self.R_PSIS = self._3(10)
        self.R_Thigh_Upper = self._3(13)
        self.R_Knee = self._3(16)
        self.R_Thigh_Rear = self._3(19)
        self.L_Thigh_Upper = self._3(22)
        self.L_Thigh_Rear = self._3(25)
        self.L_Knee = self._3(28)
        self.L_Shank_Upper = self._3(31)
        self.L_Shank_Front = self._3(34)
        self.L_Shank_Rear = self._3(37)
        self.L_Ankle = self._3(40)
        self.R_Shank_Upper = self._3(43)
        self.R_Shank_Rear = self._3(46)
        self.R_Shank_Front = self._3(49)
        self.R_Ankle = self._3(52)
        self.R_Heel = self._3(55)
        self.R_Toe_Tip = self._3(58)
        self.R_Toe_Med = self._3(61)
        self.R_Toe_Lat = self._3(64)
        self.L_Heel = self._3(67)
        self.L_Toe_Tip = self._3(70)
        self.L_Toe_Med = self._3(73)
        self.L_Toe_Lat = self._3(76)
        self.R_Thigh_Front = self._3(79)
        self.L_Thigh_Front = self._3(82)


    def _3(self, idx_start):
        return [idx_start, idx_start+1, idx_start+2]
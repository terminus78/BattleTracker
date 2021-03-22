class Mini:
    def __init__():
        self.name = name
        self.hP = hP
        self.coordinate = coordinate
        self.height = height
        self.size = size
    
    def Calculate(self, entity):
        deltaX = entity.coordinate[0] - self.coordinate[0]
        deltaY = entity.coordinate[1] - self.coordinate[1]
        deltaZ = entity.coordinate[2] - self.coordinate[2]
        
        if deltaX == 0:
            grndHypo = deltaY
        elif deltaY == 0:
            grndHypo = deltaX
        else:
            grndHypo = math.sqrt(deltaX**2 + deltaY**2)

        if grndHypo == 0:
            distance = deltaZ
        else:
            distance = math.sqrt(grndHypo**2 + deltaZ**2)
        
        return distance
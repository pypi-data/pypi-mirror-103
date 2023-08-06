import numpy as np

class ImgData:
    # def __init__(self):
    #     pass

    def loadData(self,filename):
        self.raw_data = np.loadtxt(filename)

        self.x = sorted(set(self.raw_data[:,0]))
        self.y = sorted(set(self.raw_data[:,1]))
        self.z = sorted(set(self.raw_data[:,2]))

        x_mapping = { elem:i for i, elem in enumerate(self.x)}
        y_mapping = { elem:i for i, elem in enumerate(self.y)}
        z_mapping = { elem:i for i, elem in enumerate(self.z)}

        self.number_of_params = self.raw_data.shape[1]-3
        self.all_params = []
        for i in range(self.number_of_params):
            tmp = np.empty( (len(self.x), len(self.y), len(self.z)) )
            self.all_params.append(tmp)

        for row in self.raw_data:
            x_ind = x_mapping[row[0]]
            y_ind = y_mapping[row[1]]
            z_ind = z_mapping[row[2]]

            for i in range(self.number_of_params):
                param_index = i + 3
                self.all_params[i][x_ind,y_ind,z_ind] = row[param_index]


        self.img = self.all_params[0]

    def change_param_number(self, param_number):
        self.img = self.all_params[param_number]

    def loadFakeData(self):
        self.x = np.linspace(1,10,100)
        self.y = np.linspace(50,70,500)
        self.z = np.linspace(80,150,250)
        
        # raw data from GG
        self.img = np.random.rand(len(self.x), len(self.y), len(self.z))
        self.img[0,0,0] = np.nan

    
    #xy slice
    def get_slice_parallel(self):
        scale = self.x[1]-self.x[0], self.y[1]-self.y[0]
        pos = self.x[0] - scale[0]/2, self.y[0] - scale[1]/2
        return pos, scale, np.transpose(self.img, (2,0,1))


    # xz slice
    def get_slice_perp(self):
        scale = self.x[1]-self.x[0], self.z[1]-self.z[0]
        pos = self.x[0] - scale[0]/2, self.z[0] - scale[1]/2
        return pos, scale, np.transpose(self.img, (1,0,2))


    #yz slice
    def get_slice_perp2(self):
        scale = self.y[1]-self.y[0], self.z[1]-self.z[0]
        pos = self.y[0] - scale[0]/2, self.z[0] - scale[1]/2
        return pos, scale, np.transpose(self.img, (0,1,2))
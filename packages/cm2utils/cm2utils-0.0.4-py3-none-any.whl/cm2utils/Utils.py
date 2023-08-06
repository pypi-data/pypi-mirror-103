import os, errno, re
import numpy
from scipy.linalg import qr
import math
import glob
from icecream import ic
# import matplotlib.pyplot as plt
import plotly.graph_objects as pgo
from plotly.subplots import make_subplots


class Util:
    def __init__(self):
        pass
    def address_file(self, subDir, fileName):
        #region doc. string
        """Function to get the current file location.

        - If you change the location of the "Utils.py" file, you should revise this function.

        Parameters
            - subDir - :class:`String`. sub-directory.
            - fileName - :class:`String`. file name.
        
        Returns
            - R - :class:`String`. current path + subDir + fileName.
        """
        #endregion doc. string
        
        current_dir = os.path.dirname(__file__) #<kr> 파일이 있는 곳의 폴더.
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        #parent_dir = Path(current_dir).parent
        rel_path = subDir + "/" + fileName
        abs_path = os.path.join(parent_dir, rel_path)
        
        # ⬇︎ make directory if the directory does not exist.
        if not os.path.exists(os.path.dirname(abs_path)):
            try:
                os.makedirs(os.path.dirname(abs_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        return abs_path

    def getSubfolders(self, path):
        #region doc. string
        """To get the sub folders

        Parameters
            - path - :class:`string`.
        
        Returns
            - R (self.sub) - :class:`list`. all sub folders of the given path.
        """
        #endregion doc. string
        subs = [f.path for f in os.scandir(path) if f.is_dir()]
        if len(subs) == 0:
            return self.subs
            #return Util.subs
        else:
            for i in subs:
                self.subs.append(i)
                #Util.subs.append(i)
                self.getSubfolders(i)
         
         #<kr> ⬇ 어찌 하다보니 됐는데, 재귀함수 return이 이해가 안됨. 
         #<kr> 왜 저기 위에서 return을 했는데, 또 여기서 return을 해줘야 하고, 그래야만 제대로 된 결과가 나오는지 모르겠음.
         #<kr> Java 같은거 생각해보면 여기에도 return을 해줘야 맞긴 하지만 ㅠㅠㅠ
        return self.subs
        

    def findFilesAndRemoveKRTags(self, path, extension):
        #region doc. string
        """#<kr> path에서 해당되는 extension의 모든 파일을 대상으로 <kr> 태그가 있는 줄 삭제.

        Parameters
            - path - :class:`string`.
            - extension - :class:`string`.
        
        Returns
            - void.
        """
        #endregion doc. string
        files = "*." + extension
        for filename in glob.glob(os.path.join(path, files)):
            print("File name: " + filename)
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                contents = f.read()
                result = re.sub(r'(#<kr>).*', "", contents)
                result = re.sub(r'(- #<kr>).*', "", result)
            
            #<kr> ⬇︎ 이것을 사용하면, 파일 덮어쓰기가 됨.
            # with open(os.path.join(os.getcwd() + "out", filename), 'w') as f:
            #     f.write(result)
            
            #<kr> ⬇︎ data 이후의 경로만을 가져옴. filename을 그대로 사용하면 전체 경로가 들어가서 out 폴더에 Users/PLUTON/... 등 폴더 다 생김.
            netFileName = self.__getNetFileName(filename, "data")
            #with open(Util().address_file("data/out", netFileName), 'w') as f:
            with open(Util().address_file("out", netFileName), 'w') as f:
                f.write(result)
    
    def __getNetFileName(self, entire_address, fromValue):
        #region doc. string
        """#<kr> fromValue 뒷부분의 경로 가져옴.

        Parameters
            - entire_address - :class:`[type]`. [Description].
            - fromValue - :class:`[type]`. [Description].
        
        Returns
            - R (fileName) - :class:`string`. #<kr> fromValue 이후부분의 주소. (파일명 포함)
        """
        #endregion doc. string

        #result = re.finditer(r'(\/)', entire_address)
        #<kr> ⬇︎ 이해가 잘 안됨. 아주 이상함. result의 type은 callable iterator인데, 이게 아마, 한번 돌어버리면 재사용을 못하는 듯.
        #<kr> 무슨말이냐면, result를 iterator하는 구문, 즉, for i in result 라든지 이런걸로 result 한번 사용해버리면, 또다시 result 사용 못함.
        #<kr> 그래서 뭔가 테스트한다고 쓸데없이 iterator 돌리지 말것. obsidian > code_tip 에 좀 더 자세히 적어두겠음.
        result = re.finditer(fromValue + r'(\/)', entire_address)
        last = None
        while True:
            try:
                element = next(result)
                last = element
            except:
                break
        fileName = entire_address[last.end():]
        return fileName
        #<kr> ⬆︎ while 부분은 제일 끝 요소 찾기 위해서 돌린것.


    def factorial(self, n):
        #region doc. string
        """factorial calculation. == math.factorial

        Parameters
            - n - :class:`int`.
        
        Returns
            - R - :class:`int`.
        """
        #endregion doc. string
        if n == 0:
            return 1
        else:
            return n * self.factorial(n-1)


    def inducedK(self, m, n, s_k):
        #region doc. string
        """Calculating the K value for KD tree for Meshfree analysis

        Parameters
            - m - :class:`int`. Polynomial Order
            - n - :class:`int`. Problem Dimension
            - s_k - :class:`float`. Safe factor for K
        
        Returns
            - R - :class:`int`. Induced K value for KD tree
        """
        #endregion doc. string
        return int(s_k * self.factorial(m+n) / (self.factorial(m) * self.factorial(n)))


    def mldivide(self, A, b):
        #region doc. string
        """mldivide function (\ operator) of Matlab. (solving simultaneous equations (연립방정식) A*x = B) == numpy.linalg.lstsq

        - ref site: https://pythonquestion.com/post/how-can-i-obtain-the-same-special-solutions-to-underdetermined-linear-systems-that-matlab-s-a-b-mldivide-operator-returns-using-numpy-scipy/
        - ref site: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        x1, res, rnk, s = numpy.linalg.lstsq(A, b)
        if rnk == A.shape[1]:
            return x1   # nothing more to do if A is full-rank
        Q, R, P = qr(A.T, mode='full', pivoting=True)
        Z = Q[:, rnk:].conj()
        C = numpy.linalg.solve(Z[rnk:], -x1[rnk:])
        return x1 + Z.dot(C)


    def getKeyFromValue(self, dicData, val):
        for key, value in dicData.items():
            if val == value: 
                return key 
  
        return "key doesn't exist"


    def intersectionPtBtwLineAndPt2D(self, startP, endP, exP):
        #region doc. string
        """A, B는 하나의 선분, 선분위에 있지 않는 점 P가 선분 AB에 수선의 발을 내렸을때의 교점 H 찾기. 그냥 연립방정식 푼것.
                        * B
                    -   -
              H *       -
            -       * P -
        A *--------------

        - [Description]
        - [Description]

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        denominator = startP[0] - endP[0]
        numerator = startP[1] - endP[1]
        if denominator == 0 or numerator == 0:
            return "ccccccccheck"
        else:
            alpha = abs(  (startP[1] - endP[1]  ) /  ( startP[0] - endP[0] ) )
            Hx = ( -startP[1] + exP[1] + alpha * startP[0] + (1 / alpha) * exP[0] ) / (  alpha + (1 / alpha)  )
            Hy = alpha * ( Hx - startP[0] ) + startP[1]
            return (Hx, Hy, 0)

    def euclideanDistance2D(self, startP, endP):
        v = (startP[0] - endP[0])**2 + (startP[1] - endP[1])**2
        return math.sqrt(v)

    def show3dPlots(self, data):
        #region doc. string
        """[summary]

        - [Description]
        - [Description]

        Parameters
            - data - :class:`list[list[numpy.array]]`. numpy.array (x), numpy.array (y), numpy.array (z)의 리스트의 리스트.
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        
        #region - plotting using matplotlib
        # fig = plt.figure(figsize=(16,8))
        # idx = 1
        # for i in data:
        #     ax = fig.add_subplot(1,len(data),idx, projection='3d')
        #     # surf = ax.plot_surface(i[0], i[1], i[2], rstride=1, cstride=1, cmap='seismic', alpha=0.8)
        #     # surf = ax.plot_surface(i[0], i[1], i[2], rstride=1, cstride=1, cmap='seismic')
        #     surf = ax.plot_surface(i[0], i[1], i[2], rstride=1, cstride=1, cmap='coolwarm', edgecolor='none')
        #     # surf =  ax.plot_wireframe(i[0], i[1], i[2])            
        #     # ax = plt.axes(projection='3d')
        #     # plt.contour(i[0], i[1], i[2])
        #     # ax.plot_surface(i[0], i[1], i[2], cmap='viridis')            
        #     # label
        #     ax.set_xlabel('X')
        #     ax.set_ylabel('Y')
        #     ax.set_zlabel('Z')
        #     # color bar
        #     fig.colorbar(surf, shrink=0.3, aspect=10) # aspect: Ratio of long to short dimensions.            
        #     # scale
        #     # ax.set_xlim3d(0, 100)
        #     # ax.set_ylim3d(0, 100)
        #     # ax.set_zlim3d(0, 1)            
        #     idx += 1
        # plt.show()
        #endregion - plotting using matplotlib

        # ⬇︎ subplot attributes
        cols = len(data)
        specs = []
        spec0 = []
        specString = {'is_3d': True}
        subplot_titles = []
        for i in range(cols):
            spec0.append(specString)
            subplot_titles.append(str(i+1))
        specs.append(spec0)
        fig = make_subplots(rows=1, cols=cols, specs=specs, subplot_titles=subplot_titles)
        
        idx = 1
        for i in data:
            fig.add_trace(pgo.Surface(x=i[0], y=i[1], z=i[2]), 1, idx)
            #<kr> ⬇︎ showscale 옵션이 옆에 color bar에 대한 것. 갯수가 변하는 것에 따라서 color bar 위치 맞추는 것이 쉽지 않음.그래서 그냥 없앴음.
            # fig.update_traces(colorscale='Viridis', showscale=False, contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))
            fig.update_traces(showscale=False, contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))
            # fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))
            idx += 1

        fig.update_layout(title_text="Gaussian Distributions", autosize=False, width=1600, height=800)
        fig.show()
        


    def transformFor2dLineOnXAxis(self, startP:list, endP:list, point:list, toXAxis=True):
        #region doc. string
        """[summary]

        - toXAxis = True이면, X 축으로 이동, False면, 원래 좌표로 이동.
        - [Description]

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        
        deltaX = endP[0] - startP[0]
        deltaY = endP[1] - startP[1]
        centerP = [ (endP[0] + startP[0]) / 2,  (endP[1] + startP[1]) / 2]
        theta = 0
        if deltaX == 0:
            theta =  -(numpy.pi/2)
        elif deltaY == 0:
            theta = 0
        else:
            tangentTheta = deltaY / deltaX
            if tangentTheta > 0:
                temp = numpy.arctan(tangentTheta)
                theta = -1*temp
            else:
                temp = numpy.arctan(tangentTheta)
                theta = -1 * (temp + numpy.pi)

        tR = numpy.array( [[numpy.cos(theta), -numpy.sin(theta)],  [numpy.sin(theta), numpy.cos(theta)]] )
        tT = numpy.array( [[-centerP[0]],  [-centerP[1]]] )
        p = numpy.array( [ [point[0]], [point[1]]  ] )
        if (toXAxis):
            return numpy.dot(tR, (p + tT) ) 
        return numpy.dot( numpy.linalg.inv(tR), p ) - tT

    

    def diffx(self, l1, l2):
        #region doc. string
        """두 리스트의 차집합.

        Parameters
            - li1 - :class:`list`. 차집합을 위한 첫번째 리스트.
            - li2 - :class:`list`. 차집합을 위한 두번재 리스트.
        
        Returns
            - R - :class:`list`. 차집합
        """
        #endregion doc. string
        li_dif = [i for i in l1 if i in l1 and i not in l2]
        return li_dif 

    def unionx(self, l1, l2):
        #region doc. string
        """Union of the 2 lists.

        Parameters
            - li1 - :class:`list`. list 1.
            - li2 - :class:`list`. list 2.
        
        Returns
            - R - :class:`list`. Union.
        """
        #endregion doc. string
        li_dif = [i for i in l1 if i in l1 and i in l2]
        return li_dif 


            
    def sum2MatMeshgrid(self, data1, data2):
        #region doc. string
        """meshgrid로 생성된 두개의 대칭인 gaussian functions를 하나로 합치는 것.

        - 결과가 맞는지 틀린지 애매함. 사용하지 않음. 고생해서 만들었기 때문에 그냥 놔둠.

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
                
        data1Raw = data1[0][0]
        data1RawList = data1Raw.tolist() # index를 찾기위해.

        data2Raw = data2[0][0]
        data2RawList = data2Raw.tolist() # index를 찾기위해.
        
        unionX = self.unionx(data1Raw, data2Raw)
        diff1 = self.diffx(data1Raw, data2Raw)
        diff2 = self.diffx(data2Raw, data1Raw)
        # print("u: ", unionX)
        # print("d1: ", diff1)
        # print("d2: ", diff2)
        
        newX = numpy.append(  data1Raw, diff2)
        newY = newX
        newXList = newX.tolist() # index를 찾기위해.
        
        newX_mat, newY_mat = numpy.meshgrid(newX, newY)
        newZ_mat = zRange_mat = numpy.zeros([len(newX), len(newY)])
        
        #region - 다른부분
        diff_mat_idx = []
        
        ## DONE - 제외되는 부분, diagonal 1.
        for i in diff1:
            diff_mat_idx.append([i,i])
            # data 1
            # print("data1: ", data1RawList.index(i), data1RawList.index(i))
            z1 = data1[2][data1RawList.index(i)][data1RawList.index(i)]
            # sum
            # print("sum: ", newXList.index(i), newXList.index(i))
            newZ_mat[newXList.index(i)][newXList.index(i)] = z1
        for i in diff2:
            diff_mat_idx.append([i,i])
            # data 2
            # print("data2: ", data2RawList.index(i), data2RawList.index(i))
            z2 = data2[2][data2RawList.index(i)][data2RawList.index(i)]
            # sum
            # print("sum: ", newXList.index(i), newXList.index(i))
            newZ_mat[newXList.index(i)][newXList.index(i)] = z2


        ## DONE 제외되는 부분, diagonal 2. -> 이건 "0"
        for i in diff1:
            for j in diff2:
                diff_mat_idx.append([i,j])
                diff_mat_idx.append([j,i])

        ## DONE 제외되는 부분
        for i in unionX:
            for j in diff1:
                diff_mat_idx.append([i,j])
                diff_mat_idx.append([j,i])
                # data 1
                # print("data1: ", data1RawList.index(i), data1RawList.index(j))
                z11 = data1[2][data1RawList.index(i)][data1RawList.index(j)]
                # print("data1: ", data1RawList.index(j), data1RawList.index(i))
                z12 = data1[2][data1RawList.index(j)][data1RawList.index(i)]
                # sum
                # print("sum: ", newXList.index(i), newXList.index(j))
                newZ_mat[newXList.index(i)][newXList.index(j)] = z11
                # print("sum: ", newXList.index(j), newXList.index(i))
                newZ_mat[newXList.index(j)][newXList.index(i)] = z12

            for k in diff2:
                diff_mat_idx.append([i,k])
                diff_mat_idx.append([k,i])
                # data 2
                # print("data2: ", data2RawList.index(i), data2RawList.index(k))
                z21 = data2[2][data2RawList.index(i)][data2RawList.index(k)]
                # print("data2: ", data2RawList.index(k), data2RawList.index(i))
                z22 = data2[2][data2RawList.index(k)][data2RawList.index(i)]
                # sum
                # print("sum: ", newXList.index(i), newXList.index(k))
                newZ_mat[newXList.index(i)][newXList.index(k)] = z21
                # print("sum: ", newXList.index(k), newXList.index(i))
                newZ_mat[newXList.index(k)][newXList.index(i)] = z22
        
        ## Union이 없는 경우.
        for i in diff1:
            for j in diff1:
                diff_mat_idx.append([i,j])
                diff_mat_idx.append([j,i])
                # data 1
                # print("data1: ", data1RawList.index(i), data1RawList.index(j))
                z11 = data1[2][data1RawList.index(i)][data1RawList.index(j)]
                # print("data1: ", data1RawList.index(j), data1RawList.index(i))
                z12 = data1[2][data1RawList.index(j)][data1RawList.index(i)]
                # sum
                # print("sum: ", newXList.index(i), newXList.index(j))
                newZ_mat[newXList.index(i)][newXList.index(j)] = z11
                # print("sum: ", newXList.index(j), newXList.index(i))
                newZ_mat[newXList.index(j)][newXList.index(i)] = z12
        for i in diff2:
            for k in diff2:
                # data 2
                # print("data2: ", data2RawList.index(i), data2RawList.index(k))
                z21 = data2[2][data2RawList.index(i)][data2RawList.index(k)]
                # print("data2: ", data2RawList.index(k), data2RawList.index(i))
                z22 = data2[2][data2RawList.index(k)][data2RawList.index(i)]
                # sum
                # print("sum: ", newXList.index(i), newXList.index(k))
                newZ_mat[newXList.index(i)][newXList.index(k)] = z21
                # print("sum: ", newXList.index(k), newXList.index(i))
                newZ_mat[newXList.index(k)][newXList.index(i)] = z22
        
        ## DONE - 공통부분
        for i in unionX:
            for j in unionX:
                diff_mat_idx.append([i,j])
                # print([i,j])
                # find location
                # data 1
                data1RawList = data1Raw.tolist()
                # print("data1: ", data1RawList.index(i), data1RawList.index(j))
                z1 = data1[2][data1RawList.index(i)][data1RawList.index(j)]
                # data 2
                data2RawList = data2Raw.tolist()
                # print("data2: ", data2RawList.index(i), data2RawList.index(j))
                z2 = data2[2][data2RawList.index(i)][data2RawList.index(j)]
                # sum
                # print("sum: ", newXList.index(i), newXList.index(j))
                newZ_mat[newXList.index(i)][newXList.index(j)] = z1+z2


        return newX_mat, newY_mat, newZ_mat


    def coords2MeshGrid(self, coords):
        #region doc. string
        """일반적 형식의 x, y coord를 mesh grid 형식으로 변환.

        - [Description]
        - [Description]

        Parameters
            - coords - :class:`numpy.array`. numpy.array typed coord.  - n x 2 (x, y)  OR n x 3 (x, y, z). z values are ignored.
        
        Returns
            - R1 (xGrid) - :class:`numpy.array`. MeshGrid typed X matrix.
            - R2 (yGrid) - :class:`numpy.array`. MeshGrid typed Y matrix.
        """
        #endregion doc. string

        # ⬇︎ kind="mergesort" 옵션을 넣어주어야 한번 정렬한 것을 그대로 유지하고 있음. 첫번째 컬럼, 두번째 컬럼에 대해 각각 해주어야 내가 원하는 형태로 나옴.
        sorted_allCoords = coords[numpy.argsort(coords[:, 0], kind="mergesort" )]
        sorted_allCoords = sorted_allCoords[numpy.argsort(sorted_allCoords[:, 1], kind='mergesort' )]
        
        cpsNo_y = len( set(sorted_allCoords[:,0])  )
        cpsNo_x = len( set(sorted_allCoords[:,1])  )

        xGrid = numpy.empty((cpsNo_x, cpsNo_y))
        yGrid = numpy.empty((cpsNo_x, cpsNo_y))
        
        for i in range(cpsNo_x):
            for j in range(cpsNo_y):
                xGrid[i,j] = sorted_allCoords[   cpsNo_y*i + j][0]
                yGrid[i,j] = sorted_allCoords[   cpsNo_y*i + j][1]
        
        return xGrid, yGrid


class BColor:
    end = "\033[0m"
    
    bold = "\033[1m"
    underline = "\033[4m"
    italic = "\33[3m"
    
    curl = '\33[4m'
    blink = '\33[5m'
    blink2 = '\33[6m'
    selected = '\33[7m'
    
    black = '\33[30m'
    red = "\33[31m"
    red2 = '\33[91m'
    green = '\33[32m'
    green2 = '\33[92m'
    yellow = '\33[33m'
    yellow2 = '\33[93m'
    blue = '\33[34m'
    blue2 = '\33[94m'
    violet = '\33[35m'
    violet2 = '\33[95m'
    beige = '\33[36m'
    beige2 = '\33[96m'
    white = '\33[37m'
    white2 = '\33[97m'
    grey = '\33[90m'  
    
    black_bg = '\33[40m'
    red_bg = '\33[41m'
    red_bg2 = '\33[101m'
    green_bg = '\33[42m'
    green_bg2 = '\33[102m'
    yellow_bg = '\33[43m'
    yellow_bg2 = '\33[103m'
    blue_bg = '\33[44m'
    blue_bg2 = '\33[104m'
    violet_bg = '\33[45m'
    violet_bg2 = '\33[105m'
    beige_bg = '\33[46m'
    beige_bg2 = '\33[106m'
    white_bg = '\33[47m'
    white_bg2 = '\33[107m'
    grey_bg = '\33[100m'
    
    
    
    


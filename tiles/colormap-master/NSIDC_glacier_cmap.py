
from matplotlib.colors import LinearSegmentedColormap
from numpy import nan, inf

# Used to reconstruct the colormap in viscm
parameters = {'xp': [22.674387857633945, 11.221508276482126, -14.356589454756971, -47.188177587392218, -34.590010048125208, 0.15039134803535603],
              'yp': [-20.102530541012214, -33.082460732984288, -42.24476439790574, -5.5955497382198871, 42.5065445026178, 24.563699825479944],
              'min_JK': 18.8671875,
              'max_JK': 92.5}

cm_data = [[0.75      , 0.50185189, 0.49587242],
       [0.75      , 0.50770591, 0.49574077],
       [0.75      , 0.51356221, 0.49560491],
       [0.75      , 0.51942099, 0.49546473],
       [0.75      , 0.52528242, 0.49532008],
       [0.75      , 0.53114669, 0.49517081],
       [0.75      , 0.53701401, 0.49501678],
       [0.75      , 0.54288459, 0.49485783],
       [0.75      , 0.54875866, 0.49469382],
       [0.75      , 0.55463644, 0.49452458],
       [0.75      , 0.56051819, 0.49434993],
       [0.75      , 0.56640415, 0.49416972],
       [0.75      , 0.57229461, 0.49398376],
       [0.75      , 0.57818984, 0.49379187],
       [0.75      , 0.58409014, 0.49359386],
       [0.75      , 0.58999582, 0.49338953],
       [0.75      , 0.59590721, 0.49317869],
       [0.75      , 0.60182464, 0.49296112],
       [0.75      , 0.60774848, 0.49273661],
       [0.75      , 0.61367908, 0.49250494],
       [0.75      , 0.61961685, 0.49226588],
       [0.75      , 0.6255622 , 0.49201919],
       [0.75      , 0.63151554, 0.49176464],
       [0.75      , 0.63747733, 0.49150197],
       [0.75      , 0.64344802, 0.49123092],
       [0.75      , 0.64942812, 0.49095122],
       [0.75      , 0.65541813, 0.4906626 ],
       [0.75      , 0.66141857, 0.49036478],
       [0.75      , 0.66743002, 0.49005746],
       [0.75      , 0.67345304, 0.48974034],
       [0.75      , 0.67948825, 0.4894131 ],
       [0.75      , 0.68553628, 0.48907542],
       [0.75      , 0.69159779, 0.48872698],
       [0.75      , 0.69767348, 0.48836742],
       [0.75      , 0.70376407, 0.48799639],
       [0.75      , 0.7098703 , 0.48761353],
       [0.75      , 0.71599298, 0.48721845],
       [0.75      , 0.72213291, 0.48681078],
       [0.75      , 0.72829095, 0.4863901 ],
       [0.75      , 0.734468  , 0.485956  ],
       [0.75      , 0.74066499, 0.48550806],
       [0.75      , 0.74688289, 0.48504583],
       [0.74687728, 0.75      , 0.48456886],
       [0.74061447, 0.75      , 0.48407667],
       [0.73432758, 0.75      , 0.48356879],
       [0.72801545, 0.75      , 0.4830447 ],
       [0.72167688, 0.75      , 0.4825039 ],
       [0.71531064, 0.75      , 0.48194585],
       [0.70891541, 0.75      , 0.48137001],
       [0.70248985, 0.75      , 0.48077579],
       [0.69603252, 0.75      , 0.48016262],
       [0.68954198, 0.75      , 0.4795299 ],
       [0.68301667, 0.75      , 0.47887699],
       [0.676455  , 0.75      , 0.47820326],
       [0.66985531, 0.75      , 0.47750804],
       [0.66321585, 0.75      , 0.47679064],
       [0.65653483, 0.75      , 0.47605037],
       [0.64981036, 0.75      , 0.47528648],
       [0.64304049, 0.75      , 0.47449823],
       [0.63622317, 0.75      , 0.47368483],
       [0.62935627, 0.75      , 0.47284549],
       [0.6224376 , 0.75      , 0.47197938],
       [0.61546484, 0.75      , 0.47108565],
       [0.60843561, 0.75      , 0.47016341],
       [0.6013474 , 0.75      , 0.46921175],
       [0.59419762, 0.75      , 0.46822974],
       [0.58698358, 0.75      , 0.46721641],
       [0.57970245, 0.75      , 0.46617075],
       [0.57235133, 0.75      , 0.46509175],
       [0.56492715, 0.75      , 0.46397833],
       [0.55742677, 0.75      , 0.46282939],
       [0.54984688, 0.75      , 0.46164382],
       [0.54218407, 0.75      , 0.46042042],
       [0.53443476, 0.75      , 0.45915801],
       [0.52659525, 0.75      , 0.45785532],
       [0.51866169, 0.75      , 0.45651109],
       [0.51063006, 0.75      , 0.45512399],
       [0.50249621, 0.75      , 0.45369264],
       [0.49425578, 0.75      , 0.45221564],
       [0.48590429, 0.75      , 0.45069153],
       [0.47743703, 0.75      , 0.4491188 ],
       [0.46884914, 0.75      , 0.44749591],
       [0.46013556, 0.75      , 0.44582126],
       [0.45129101, 0.75      , 0.4440932 ],
       [0.44231002, 0.75      , 0.44231002],
       [0.44046996, 0.75      , 0.44775302],
       [0.43857121, 0.75      , 0.45322668],
       [0.4366119 , 0.75      , 0.45873342],
       [0.4345901 , 0.75      , 0.46427574],
       [0.43250381, 0.75      , 0.4698563 ],
       [0.43035098, 0.75      , 0.4754779 ],
       [0.42812948, 0.75      , 0.48114345],
       [0.42583712, 0.75      , 0.48685602],
       [0.42347165, 0.75      , 0.49261883],
       [0.42103073, 0.75      , 0.49843527],
       [0.41851196, 0.75      , 0.50430886],
       [0.41591285, 0.75      , 0.51024334],
       [0.41323084, 0.75      , 0.51624258],
       [0.41046328, 0.75      , 0.52231067],
       [0.40760745, 0.75      , 0.52845188],
       [0.40466053, 0.75      , 0.53467068],
       [0.40161962, 0.75      , 0.54097177],
       [0.39848172, 0.75      , 0.54736005],
       [0.39524373, 0.75      , 0.55384065],
       [0.39190246, 0.75      , 0.56041895],
       [0.38845462, 0.75      , 0.56710057],
       [0.38489681, 0.75      , 0.5738914 ],
       [0.38122553, 0.75      , 0.58079759],
       [0.37743714, 0.75      , 0.58782558],
       [0.37352792, 0.75      , 0.59498209],
       [0.36949402, 0.75      , 0.60227415],
       [0.36533145, 0.75      , 0.60970912],
       [0.36103611, 0.75      , 0.61729467],
       [0.35660377, 0.75      , 0.62503885],
       [0.35203006, 0.75      , 0.63295002],
       [0.34731047, 0.75      , 0.64103695],
       [0.34244034, 0.75      , 0.64930879],
       [0.33741488, 0.75      , 0.65777509],
       [0.33222912, 0.75      , 0.66644582],
       [0.32687797, 0.75      , 0.67533141],
       [0.32135613, 0.75      , 0.6844427 ],
       [0.31565817, 0.75      , 0.69379106],
       [0.30977848, 0.75      , 0.70338831],
       [0.30371124, 0.75      , 0.71324681],
       [0.29745049, 0.75      , 0.72337944],
       [0.29099005, 0.75      , 0.73379965],
       [0.28432355, 0.75      , 0.74452145],
       [0.27744441, 0.74444052, 0.75      ],
       [0.27034586, 0.73307103, 0.75      ],
       [0.2630209 , 0.72135417, 0.75      ],
       [0.25546231, 0.70927337, 0.75      ],
       [0.24766262, 0.69681134, 0.75      ],
       [0.23961417, 0.68395007, 0.75      ],
       [0.231309  , 0.67067079, 0.75      ],
       [0.22273893, 0.65695393, 0.75      ],
       [0.21389552, 0.6427791 , 0.75      ],
       [0.20477004, 0.62812507, 0.75      ],
       [0.1953535 , 0.61296969, 0.75      ],
       [0.18563661, 0.59728991, 0.75      ],
       [0.17560979, 0.5810617 , 0.75      ],
       [0.16526316, 0.56426006, 0.75      ],
       [0.15458652, 0.54685893, 0.75      ],
       [0.14356935, 0.52883117, 0.75      ],
       [0.13220077, 0.51014853, 0.75      ],
       [0.12046958, 0.49078159, 0.75      ],
       [0.10836422, 0.47069972, 0.75      ],
       [0.09587276, 0.44987103, 0.75      ],
       [0.08298287, 0.42826233, 0.75      ],
       [0.06968185, 0.40583905, 0.75      ],
       [0.05595658, 0.38256525, 0.75      ],
       [0.04179354, 0.35840349, 0.75      ],
       [0.02717876, 0.33331482, 0.75      ],
       [0.01209784, 0.3072587 , 0.75      ],
       [0.        , 0.28235294, 0.75      ],
       [0.        , 0.26470588, 0.75      ],
       [0.        , 0.24705882, 0.75      ],
       [0.        , 0.22941176, 0.75      ],
       [0.        , 0.21176471, 0.75      ],
       [0.        , 0.19411765, 0.75      ],
       [0.        , 0.17647059, 0.75      ],
       [0.        , 0.15882353, 0.75      ],
       [0.        , 0.14117647, 0.75      ],
       [0.        , 0.12352941, 0.75      ],
       [0.        , 0.10588235, 0.75      ],
       [0.        , 0.08823529, 0.75      ],
       [0.        , 0.07058824, 0.75      ],
       [0.        , 0.05294118, 0.75      ],
       [0.        , 0.03529412, 0.75      ],
       [0.        , 0.01764706, 0.75      ],
       [0.        , 0.        , 0.75      ],
       [0.01764706, 0.        , 0.75      ],
       [0.03529412, 0.        , 0.75      ],
       [0.05294118, 0.        , 0.75      ],
       [0.07058824, 0.        , 0.75      ],
       [0.08823529, 0.        , 0.75      ],
       [0.10588235, 0.        , 0.75      ],
       [0.12352941, 0.        , 0.75      ],
       [0.14117647, 0.        , 0.75      ],
       [0.15882353, 0.        , 0.75      ],
       [0.17647059, 0.        , 0.75      ],
       [0.19411765, 0.        , 0.75      ],
       [0.21176471, 0.        , 0.75      ],
       [0.22941176, 0.        , 0.75      ],
       [0.24705882, 0.        , 0.75      ],
       [0.26470588, 0.        , 0.75      ],
       [0.28235294, 0.        , 0.75      ],
       [0.3       , 0.        , 0.75      ],
       [0.31764706, 0.        , 0.75      ],
       [0.33529412, 0.        , 0.75      ],
       [0.35294118, 0.        , 0.75      ],
       [0.37058824, 0.        , 0.75      ],
       [0.38823529, 0.        , 0.75      ],
       [0.40588235, 0.        , 0.75      ],
       [0.42352941, 0.        , 0.75      ],
       [0.44117647, 0.        , 0.75      ],
       [0.45882353, 0.        , 0.75      ],
       [0.47647059, 0.        , 0.75      ],
       [0.49411765, 0.        , 0.75      ],
       [0.51176471, 0.        , 0.75      ],
       [0.52941176, 0.        , 0.75      ],
       [0.54705882, 0.        , 0.75      ],
       [0.56470588, 0.        , 0.75      ],
       [0.58235294, 0.        , 0.75      ],
       [0.6       , 0.        , 0.75      ],
       [0.61764706, 0.        , 0.75      ],
       [0.63529412, 0.        , 0.75      ],
       [0.65294118, 0.        , 0.75      ],
       [0.67058824, 0.        , 0.75      ],
       [0.68823529, 0.        , 0.75      ],
       [0.70588235, 0.        , 0.75      ],
       [0.72352941, 0.        , 0.75      ],
       [0.74117647, 0.        , 0.75      ],
       [0.75      , 0.        , 0.74117647],
       [0.75      , 0.        , 0.72352941],
       [0.75      , 0.        , 0.70588235],
       [0.75      , 0.        , 0.68823529],
       [0.75      , 0.        , 0.67058824],
       [0.75      , 0.        , 0.65294118],
       [0.75      , 0.        , 0.63529412],
       [0.75      , 0.        , 0.61764706],
       [0.75      , 0.        , 0.6       ],
       [0.75      , 0.        , 0.58235294],
       [0.75      , 0.        , 0.56470588],
       [0.75      , 0.        , 0.54705882],
       [0.75      , 0.        , 0.52941176],
       [0.75      , 0.        , 0.51176471],
       [0.75      , 0.        , 0.49411765],
       [0.75      , 0.        , 0.47647059],
       [0.75      , 0.        , 0.45882353],
       [0.75      , 0.        , 0.44117647],
       [0.75      , 0.        , 0.42352941],
       [0.75      , 0.        , 0.40588235],
       [0.75      , 0.        , 0.38823529],
       [0.75      , 0.        , 0.37058824],
       [0.75      , 0.        , 0.35294118],
       [0.75      , 0.        , 0.33529412],
       [0.75      , 0.        , 0.31764706],
       [0.75      , 0.        , 0.3       ],
       [0.75      , 0.        , 0.28235294],
       [0.75      , 0.        , 0.26470588],
       [0.75      , 0.        , 0.24705882],
       [0.75      , 0.        , 0.22941176],
       [0.75      , 0.        , 0.21176471],
       [0.75      , 0.        , 0.19411765],
       [0.75      , 0.        , 0.17647059],
       [0.75      , 0.        , 0.15882353],
       [0.75      , 0.        , 0.14117647],
       [0.75      , 0.        , 0.12352941],
       [0.75      , 0.        , 0.10588235],
       [0.75      , 0.        , 0.08823529],
       [0.75      , 0.        , 0.07058824],
       [0.75      , 0.        , 0.05294118],
       [0.75      , 0.        , 0.03529412],
       [0.75      , 0.        , 0.01764706],
       [0.75      , 0.        , 0.        ]]

test_cm = LinearSegmentedColormap.from_list(__file__, cm_data)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        from viscm import viscm
        viscm(test_cm)
    except ImportError:
        print("viscm not found, falling back on simple display")
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',
                   cmap=test_cm)
    plt.show()

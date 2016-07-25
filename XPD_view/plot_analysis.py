<<<<<<< HEAD
import matplotlib.pyplot as plt
from analysis_concurrent import analysis_concurrent
#from file import get_files
import multiprocessing


class reducedRepPlot:

    def __init__(self, tif_list, x_start, x_stop, y_start, y_stop, selection):
        """
        constructor for reducedRepPlot object
        :param file_path: path to file directory
        :type file_path: str
        :param x_start: start val for x analysis
        :param x_stop: stop val for x analysis
        :param y_start:
        :param y_stop:
        """

        #self.tif_list = get_files(file_path)
        self.tif_list = tif_list




        assert x_start >= 0 and x_start < x_stop
        assert x_stop <= 2048 #TODO change so resolution is flexible
        assert y_start >= 0 and y_start < y_stop
        assert y_stop <= 2048 #TODO change so resolution is flexible

        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.selection = selection

    def selectionSort(self, alist):
        for fillslot in range(len(alist) - 1, 0, -1):
            positionOfMax = 0
            for location in range(1, fillslot + 1):
                if alist[location][0] > alist[positionOfMax][0]:
                    positionOfMax = location

            temp = alist[fillslot]
            alist[fillslot] = alist[positionOfMax]
            alist[positionOfMax] = temp
        for arr in alist:
            arr.pop(0)
        return alist

    # def check_lists(self, list, nested_list, cpu_num):
    #     flattened_list = [val for sublist in nested_list for val in sublist]
    #     for i in range(0,cpu_num):
    #         flattened_list.remove(i)
    #
    #     print(flattened_list == list)

    def plot(self):
        """
        This function will plot analysis data as a funciton of the number of images. uses multiprocessing to speed things up
        :return: void
        """
        a = analysis_concurrent(self.y_start, self.y_stop, self.x_start, self.x_stop, self.selection)
        trunc_list = []
        cpu_count = multiprocessing.cpu_count()
        temp_list = []
        for i in range(0, cpu_count):

            if i == cpu_count-1:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : (((1+i)*len(self.tif_list)//cpu_count) +
                                                                               (len(self.tif_list)%cpu_count))]
                temp_list.insert(0, i)

            else:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : ((1+i)*len(self.tif_list)//cpu_count)]
                temp_list.insert(0, i)
            trunc_list.append(temp_list)

       # print(self.check_lists(self.tif_list, trunc_list, cpu_count))

        process_list = []
        x = range(0,len(self.tif_list))
        y = []
        q = multiprocessing.Queue()
        #a = multiprocessing.Array()
        l = multiprocessing.Lock()
        #p = multiprocessing.Process(a.x_and_y_vals, args=(l,))


        for i in range(0, cpu_count):
            process_list.append(multiprocessing.Process(target=a.x_and_y_vals, args=(l, q, trunc_list[i])))

        for process in process_list:
            process.start()
            y.append(q.get())
        for process in process_list:
            # y.append(q.get())
            process.join()


        # for i in range(0,cpu_count):
        #     y.append(q.get())

        y = self.selectionSort(y)
        flattened_y = [val for sublist in y for val in sublist]

        assert len(flattened_y) == len(self.tif_list)
        plt.scatter(x, flattened_y)

        plt.xlabel("file num")
        plt.ylabel(self.selection)

      #  plt.xscale()

        plt.show()
import matplotlib.pyplot as plt
from analysis_concurrent import analysis_concurrent
#from file import get_files
import multiprocessing


class reducedRepPlot:

    def __init__(self, tif_list, x_start, x_stop, y_start, y_stop, selection):
        """
        constructor for reducedRepPlot object
        :param file_path: path to file directory
        :type file_path: str
        :param x_start: start val for x analysis
        :param x_stop: stop val for x analysis
        :param y_start:
        :param y_stop:
        """

        #self.tif_list = get_files(file_path)
        self.tif_list = tif_list




        assert x_start >= 0 and x_start < x_stop
        assert x_stop <= 2048 #TODO change so resolution is flexible
        assert y_start >= 0 and y_start < y_stop
        assert y_stop <= 2048 #TODO change so resolution is flexible

        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.selection = selection

    def selectionSort(self, alist):
        for fillslot in range(len(alist) - 1, 0, -1):
            positionOfMax = 0
            for location in range(1, fillslot + 1):
                if alist[location][0] > alist[positionOfMax][0]:
                    positionOfMax = location

            temp = alist[fillslot]
            alist[fillslot] = alist[positionOfMax]
            alist[positionOfMax] = temp
        for arr in alist:
            arr.pop(0)
        return alist

    # def check_lists(self, list, nested_list, cpu_num):
    #     flattened_list = [val for sublist in nested_list for val in sublist]
    #     for i in range(0,cpu_num):
    #         flattened_list.remove(i)
    #
    #     print(flattened_list == list)

    def plot(self):
        """
        This function will plot analysis data as a funciton of the number of images. uses multiprocessing to speed things up
        :return: void
        """
        a = analysis_concurrent(self.y_start, self.y_stop, self.x_start, self.x_stop, self.selection)
        trunc_list = []
        cpu_count = 10 #2 * multiprocessing.cpu_count()
        temp_list = []
        for i in range(0, cpu_count):

            if i == cpu_count-1:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : (((1+i)*len(self.tif_list)//cpu_count) +
                                                                               (len(self.tif_list)%cpu_count))]
                temp_list.insert(0, i)

            else:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : ((1+i)*len(self.tif_list)//cpu_count)]
                temp_list.insert(0, i)
            trunc_list.append(temp_list)

       # print(self.check_lists(self.tif_list, trunc_list, cpu_count))

        process_list = []
        x = range(0,len(self.tif_list))
        y = []
        q = multiprocessing.Queue()
        l = multiprocessing.Lock()
        #p = multiprocessing.Process(a.x_and_y_vals, args=(l,))


        for i in range(0, cpu_count):
            process_list.append(multiprocessing.Process(target=a.x_and_y_vals, args=(l, q, trunc_list[i])))

        for process in process_list:
            process.start()

        for process in process_list:
            y.append(q.get())
            process.join()




        y = self.selectionSort(y)
        flattened_y = [val for sublist in y for val in sublist]

        assert len(flattened_y) == len(self.tif_list)
        plt.scatter(x, flattened_y)

        plt.xlabel("file num")
        plt.ylabel(self.selection)

      #  plt.xscale()

        plt.show()
=======
<<<<<<< HEAD
import matplotlib.pyplot as plt
from analysis_concurrent import analysis_concurrent
#from file import get_files
import multiprocessing


class reducedRepPlot:

    def __init__(self, tif_list, x_start, x_stop, y_start, y_stop, selection):
        """
        constructor for reducedRepPlot object
        :param file_path: path to file directory
        :type file_path: str
        :param x_start: start val for x analysis
        :param x_stop: stop val for x analysis
        :param y_start:
        :param y_stop:
        """

        #self.tif_list = get_files(file_path)
        self.tif_list = tif_list




        assert x_start >= 0 and x_start < x_stop
        assert x_stop <= 2048 #TODO change so resolution is flexible
        assert y_start >= 0 and y_start < y_stop
        assert y_stop <= 2048 #TODO change so resolution is flexible

        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.selection = selection

    def selectionSort(self, alist):
        for fillslot in range(len(alist) - 1, 0, -1):
            positionOfMax = 0
            for location in range(1, fillslot + 1):
                if alist[location][0] > alist[positionOfMax][0]:
                    positionOfMax = location

            temp = alist[fillslot]
            alist[fillslot] = alist[positionOfMax]
            alist[positionOfMax] = temp
        for arr in alist:
            arr.pop(0)
        return alist

    # def check_lists(self, list, nested_list, cpu_num):
    #     flattened_list = [val for sublist in nested_list for val in sublist]
    #     for i in range(0,cpu_num):
    #         flattened_list.remove(i)
    #
    #     print(flattened_list == list)

    def plot(self):
        """
        This function will plot analysis data as a funciton of the number of images. uses multiprocessing to speed things up
        :return: void
        """
        a = analysis_concurrent(self.y_start, self.y_stop, self.x_start, self.x_stop, self.selection)
        trunc_list = []
        cpu_count = 10 #multiprocessing.cpu_count()
        temp_list = []
        for i in range(0, cpu_count):

            if i == cpu_count-1:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : (((1+i)*len(self.tif_list)//cpu_count) +
                                                                               (len(self.tif_list)%cpu_count))]
                temp_list.insert(0, i)

            else:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : ((1+i)*len(self.tif_list)//cpu_count)]
                temp_list.insert(0, i)
            trunc_list.append(temp_list)

       # print(self.check_lists(self.tif_list, trunc_list, cpu_count))

        process_list = []
        x = range(0,len(self.tif_list))
        y = []
        q = multiprocessing.Queue()
        #a = multiprocessing.Array()
        l = multiprocessing.Lock()
        #p = multiprocessing.Process(a.x_and_y_vals, args=(l,))


        for i in range(0, cpu_count):
            process_list.append(multiprocessing.Process(target=a.x_and_y_vals, args=(l, q, trunc_list[i])))

        for process in process_list:
            process.start()

        for process in process_list:
            y.append(q.get())
            process.join()


        # for i in range(0,cpu_count):
        #     y.append(q.get())

        y = self.selectionSort(y)
        flattened_y = [val for sublist in y for val in sublist]

        assert len(flattened_y) == len(self.tif_list)
        plt.scatter(x, flattened_y)

        plt.xlabel("file num")
        plt.ylabel(self.selection)

      #  plt.xscale()

        plt.show()
=======
import matplotlib.pyplot as plt
from analysis_concurrent import analysis_concurrent
#from file import get_files
import multiprocessing


class reducedRepPlot:

    def __init__(self, tif_list, x_start, x_stop, y_start, y_stop, selection):
        """
        constructor for reducedRepPlot object
        :param file_path: path to file directory
        :type file_path: str
        :param x_start: start val for x analysis
        :param x_stop: stop val for x analysis
        :param y_start:
        :param y_stop:
        """

        #self.tif_list = get_files(file_path)
        self.tif_list = tif_list




        assert x_start >= 0 and x_start < x_stop
        assert x_stop <= 2048 #TODO change so resolution is flexible
        assert y_start >= 0 and y_start < y_stop
        assert y_stop <= 2048 #TODO change so resolution is flexible

        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.selection = selection

    def selectionSort(self, alist):
        for fillslot in range(len(alist) - 1, 0, -1):
            positionOfMax = 0
            for location in range(1, fillslot + 1):
                if alist[location][0] > alist[positionOfMax][0]:
                    positionOfMax = location

            temp = alist[fillslot]
            alist[fillslot] = alist[positionOfMax]
            alist[positionOfMax] = temp
        for arr in alist:
            arr.pop(0)
        return alist

    # def check_lists(self, list, nested_list, cpu_num):
    #     flattened_list = [val for sublist in nested_list for val in sublist]
    #     for i in range(0,cpu_num):
    #         flattened_list.remove(i)
    #
    #     print(flattened_list == list)

    def plot(self):
        """
        This function will plot analysis data as a funciton of the number of images. uses multiprocessing to speed things up
        :return: void
        """
        a = analysis_concurrent(self.y_start, self.y_stop, self.x_start, self.x_stop, self.selection)
        trunc_list = []
        cpu_count = 2 * multiprocessing.cpu_count()
        temp_list = []
        for i in range(0, cpu_count):

            if i == cpu_count-1:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : (((1+i)*len(self.tif_list)//cpu_count) +
                                                                               (len(self.tif_list)%cpu_count))]
                temp_list.insert(0, i)

            else:
                temp_list = self.tif_list[(i*len(self.tif_list)//cpu_count) : ((1+i)*len(self.tif_list)//cpu_count)]
                temp_list.insert(0, i)
            trunc_list.append(temp_list)

       # print(self.check_lists(self.tif_list, trunc_list, cpu_count))

        process_list = []
        x = range(0,len(self.tif_list))
        y = []
        q = multiprocessing.Queue()
        l = multiprocessing.Lock()
        #p = multiprocessing.Process(a.x_and_y_vals, args=(l,))


        for i in range(0, cpu_count):
            process_list.append(multiprocessing.Process(target=a.x_and_y_vals, args=(l, q, trunc_list[i])))

        for process in process_list:
            process.start()

        for process in process_list:
            process.join()


        for i in range(0,cpu_count):
            y.append(q.get())

        y = self.selectionSort(y)
        flattened_y = [val for sublist in y for val in sublist]

        assert len(flattened_y) == len(self.tif_list)
        plt.scatter(x, flattened_y)

        plt.xlabel("file num")
        plt.ylabel(self.selection)

      #  plt.xscale()

        plt.show()
>>>>>>> 3ad69f1f78d7ce3eca99599697fd0d35d153c771

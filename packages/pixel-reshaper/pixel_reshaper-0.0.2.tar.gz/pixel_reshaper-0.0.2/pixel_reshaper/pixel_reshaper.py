import numpy as np
from PIL import Image
import random, csv, os, shutil

def unpack_images(classNames, loc, dirName, splitPercent, dimImage, fileName, containsLabels=True, colorEncode='RGB', pixDtype='float64'):
    """
    Unpack an image dataset stored as raw data (csv or otherwise) into .png's. 
    Creates file structure for easy data loading and handles train/test
    splitting internally.

    Time complexity - O(3k+N) for classes k, rows N.

    Parameters
    ----------
    classNames : list
        list of class names
    loc : str
        location to unpack to
    dirName : str 
        name of directory to create when unpacking data
    splitPercent : float 
        decimal representing percentage of data to retain for test set
    dimImage : tuple
        a tuple of integers such that (h, w, c) corresponds to height, width and channels
    fileName : str
        data file name, expects .csv in semi-colon, comma, pipe or tsv format
    containsLabels : bool
        denotes if labels are present in the dataset, default False, expected label column index = [-1]
    colorEncode : str
        color encoding for the resulting image, default 'RGB'
    pixDtype : str
        expected data type for pixels, default 'float64'

    Returns
    -------
    str
        file path to the directory containing generated images
    """

    counter = {}
    labelMap = {}
    filePathMap = {
        0:{}, 
        1:{}
    }
    classFilePaths = {
        'train':[], 
        'test':[]
    }
    
    for i, j in enumerate(classNames):
        labelMap[str(i)] = j
        filePathMap[0][str(i)] = ''
        filePathMap[1][str(i)] = ''

    #Paths for the directory
    parentPath = os.path.join(loc, dirName)
    trainPath = os.path.join(parentPath, 'train')
    testPath = os.path.join(parentPath, 'test')
    try:
        os.mkdir(parentPath)
        os.mkdir(trainPath)
        os.mkdir(testPath)
        print(f'Directory \'{dirName}\' created')
        for cl in classNames:
            fpTrain = os.path.join(trainPath, cl)
            fpTest = os.path.join(testPath, cl)
            classFilePaths['train'].append(fpTrain)
            classFilePaths['test'].append(fpTest)
            os.mkdir(fpTrain)
            os.mkdir(fpTest)
            print(f'    {cl} class train/test directories created')
            
        for i, itemTrain, itemTest in zip(range(len(classNames)), classFilePaths['train'], classFilePaths['test']):
            i = str(i)
            filePathMap[0][i] = itemTrain
            filePathMap[1][i] = itemTest

    except FileExistsError:
        print(f'{dirName} already exists - consider deleting the directory for a clean install!')
    
    print(f'Unpacking {fileName}...\nPlease wait...')
    with open(fileName) as csv_file:
        numSamples = sum(1 for line in csv_file)-1
        test_idx = [random.randint(0, numSamples) for i in range(int(numSamples * splitPercent))]
        delim = csv.Sniffer().sniff(csv_file.read(), delimiters=';,\t|')
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file, delim)

        next(csv_reader)
        fileCount = 0
        for row in csv_reader:
            
            if fileCount % 1000 == 0: print(f'Unpacking {fileCount}/{numSamples}...', end=' ')
            
            if containsLabels: row = row[:-1]
             
            pixels = np.array(row, dtype='float64')
            pixels = pixels.reshape(dimImage)
            image = Image.fromarray(pixels, colorEncode)

            label = row[-1][0]

            if label not in counter: counter[label] = 0
            counter[label] += 1

            filename = f'{labelMap[label]}{counter[label]}.png'

            if fileCount in test_idx:
                filepath = os.path.join(filePathMap[1][label], filename)

            else:
                filepath = os.path.join(filePathMap[0][label], filename)

            image.save(filepath)
            
            if (fileCount % 999 == 0) and (fileCount != 9): print(f'Completed')
            fileCount += 1

        print(f'Unpacking complete. {fileCount} images parsed.')
        print(f'Directory located at {parentPath}')
    
    return parentPath

def parse_and_dump(loc, dirName, dimImage, pixels=None, active='current', colorEncode='RGB'):
    """
    A lightweight handball function for reading single observation tabular data and converting to
    image representation, i.e. websocket datastream. Tailored to a pytorch implementation
    with an active/archive file system where current 'of-interest' image is handled in a directory 
    of 1 that is utilised by a classifier, then moved to archive to maintain small dataloader sizes.

    Parameters
    ----------
    loc : str
        location to unpack to
    dirName : str 
        name of directory to create when unpacking data
    dimImage : tuple
        a tuple of integers such that (h, w, c) corresponds to height, width and channels
    pixels : array-like
        array of pixel values to reshape
    active : str
        name of active folder
    colorEncode : str
        expected color encoding for resulting image

    Returns
    -------
    str
        file path to the directory containing the single image for loading
    """

    parentPath = os.path.join(loc, dirName)
    currentPath = os.path.join(parentPath, active)
    dumpPath = os.path.join(parentPath, 'archive')
    try:
        os.mkdir(parentPath)
        os.mkdir(currentPath)
        os.mkdir(dumpPath)

        print(f'Directory \'{dirName}\' created')

    except FileExistsError:
        print(f'{dirName} already exists - pushing image to {currentPath}')

    if active == 'current':
        filename = 'prediction.png'
        filepath = os.path.join(currentPath, filename)

        pixels = pixels.reshape(dimImage)
        image = Image.fromarray(pixels, colorEncode)

        image.save(filepath)
        print(f'Image saved to {currentPath}')

    else:
        num_in_dir = len(os.listdir(dumpPath))
        filename = f'prection{num_in_dir + 1}.png'
        filepath = os.path.join(dumpPath, filename)

        shutil.move(currentPath+'/prediction.png', filepath)
        print(f'Image moved to {dumpPath}')

    return currentPath


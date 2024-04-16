from read2 import give_array2
from read import give_array
import win32com.client as wc
import ntpath

def model(filename):

    #split file name
    head, tail = ntpath.split(filename)

    # open Autodesk Inventor and set
    invApp = wc.Dispatch("Inventor.Application")
    invApp.Visible = True
    invDoc = invApp.Documents.Add(12290, invApp.FileManager.GetTemplateFile(12290, 8962), True)
    invPartDoc = wc.CastTo(invDoc, 'PartDocument')


    #choose plane
    xyPlane = invPartDoc.ComponentDefinition.WorkPlanes.Item(3)

    #variables needed for drawing
    tg = invApp.TransientGeometry
    tgcordinates = []


    #Collection needed for offset
    collections = invApp.TransientObjects.CreateObjectCollection()
    #necessary value assignments
    offset_distance = 0.22/10
    extrude_distance = 0.2/10


    def down(coordinates1):

        #variables needed for extrusion
        sketch_counter = 0
        sketch_distance = 0
        offset = True
        normal = True

        #surface selection for drawing
        sketch = invPartDoc.ComponentDefinition.Sketches.Add(xyPlane)
        points = sketch.SketchPoints
        lines = sketch.SketchLines

        #to hold temporary values
        dummy = []

        #if our drawing does not start from the first layer
        if coordinates1[0] == []:
            for i in range(len(coordinates1)):
                if coordinates1[i] == []:
                    if offset == True:
                        sketch_counter += 1
                else:
                    offset = False
                    dummy.append(coordinates1[i])
            if dummy != []:
                sketch_counter += 1
                coordinates1 = dummy


        #if the middle layers are empty. Draw the bottom layers, skip the empty layers and continue.
        else:
            control = False
            for i in range(len(coordinates1)):
                if coordinates1[i] == []:
                    sketch_counter += 1
                    control = True
                    normal = False
                else:
                    if control:
                        try:
                            # which layer are we on
                            i = 0
                            # how many times extrusion will be done
                            extrude_zahl = 1

                            while i < len(dummy):

                                # temporary variables for layer control
                                start = True
                                var = 0

                                #layer generation
                                if i > 0:
                                    plane = invPartDoc.ComponentDefinition.WorkPlanes.AddByPlaneAndOffset(sketch,
                                                                                                          extrude_distance * extrude_zahl,
                                                                                                          True)
                                    sketch = invPartDoc.ComponentDefinition.Sketches.Add(plane)
                                    points = sketch.SketchPoints
                                    lines = sketch.SketchLines
                                    extrude_zahl = 1

                                #draw
                                for j in range(len(dummy[i])):

                                    if dummy[i][j][0] == None:

                                        for k in range(len(tgcordinates) - 1):
                                            line1 = lines.AddByTwoPoints(tgcordinates[k], tgcordinates[k + 1])
                                            collections.Add(line1)
                                        tgcordinates.clear()

                                    else:

                                        if ((dummy[i][0][0] == dummy[i][j][0]) and (
                                                dummy[i][0][1] == dummy[i][j][1]) and start == False):
                                            line1 = lines.AddByTwoPoints(tgcordinates[j - 1], tgcordinates[0])
                                            collections.Add(line1)
                                        else:

                                            tgcordinates.append(
                                                points.Add(
                                                    tg.CreatePoint2d(dummy[i][j][0], dummy[i][j][1])))
                                            start = False
                                #offset
                                for j in range(len(tgcordinates) - 1):
                                    line1 = lines.AddByTwoPoints(tgcordinates[j], tgcordinates[j + 1])
                                    collections.Add(line1)
                                sketch.OffsetSketchEntitiesUsingDistance(collections, offset_distance, False)

                                # layer similarity check
                                while i + 1 < len(dummy) and dummy[i] == dummy[i + 1]:
                                    extrude_zahl += 1
                                    i += 1
                                    var += 1

                                #collection and array reset
                                for item in collections:
                                    item.Delete()
                                collections.Clear()
                                tgcordinates.clear()

                                #extrusion
                                profile1 = sketch.Profiles.AddForSolid()
                                extrude_feat = invPartDoc.ComponentDefinition.Features.ExtrudeFeatures
                                extrude_def = extrude_feat.CreateExtrudeDefinition(profile1,
                                                                                   wc.constants.kJoinOperation)
                                sketch_distance += extrude_zahl
                                extrude_def.SetDistanceExtent(extrude_distance * extrude_zahl, 20993)
                                extrude_feat.Add(extrude_def)

                                #variables for extruison
                                i -= var
                                i += extrude_zahl

                        except Exception as e:
                            print(f"An error occurred: {e}")
                        control = False
                        dummy = []
                    if coordinates1[i] != []:
                        dummy.append(coordinates1[i])

            if dummy != [] and not normal:
                dummy.append(coordinates1[i])
                coordinates1 = dummy

        #layer adjustments
        if sketch_counter > 0:
            sketch_counter += sketch_distance - 1
            plane = invPartDoc.ComponentDefinition.WorkPlanes.AddByPlaneAndOffset(sketch,
                                                                                  extrude_distance * sketch_counter,
                                                                                  True)
            sketch = invPartDoc.ComponentDefinition.Sketches.Add(plane)
            points = sketch.SketchPoints
            lines = sketch.SketchLines
        try:
            #which layer are we on
            i = 0
            #how many times extrusion will be done
            extrude_zahl = 1


            while i < len(coordinates1):


                #temporary variables for layer control
                start = True
                var = 0

                #layer generation
                if i > 0:
                    plane = invPartDoc.ComponentDefinition.WorkPlanes.AddByPlaneAndOffset(sketch, extrude_distance * extrude_zahl, True)
                    sketch = invPartDoc.ComponentDefinition.Sketches.Add(plane)
                    points = sketch.SketchPoints
                    lines = sketch.SketchLines
                    extrude_zahl = 1

                #making the drawing
                for j in range(len(coordinates1[i])):
                    if coordinates1[i][j][0] == None:

                        for k in range(len(tgcordinates) - 1):

                            line1 = lines.AddByTwoPoints(tgcordinates[k], tgcordinates[k + 1])
                            collections.Add(line1)
                        tgcordinates.clear()

                    else:

                        if ((coordinates1[i][0][0] == coordinates1[i][j][0]) and (
                                coordinates1[i][0][1] == coordinates1[i][j][1]) and start == False):
                            line1 = lines.AddByTwoPoints(tgcordinates[j - 1], tgcordinates[0])
                            collections.Add(line1)
                        else:

                            tgcordinates.append(
                                points.Add(tg.CreatePoint2d(coordinates1[i][j][0], coordinates1[i][j][1])))
                            start = False

                #offset
                for j in range(len(tgcordinates) - 1):
                    line1 = lines.AddByTwoPoints(tgcordinates[j], tgcordinates[j + 1])
                    collections.Add(line1)
                sketch.OffsetSketchEntitiesUsingDistance(collections, offset_distance, False)

                #layer similarity check
                while i + 1 < len(coordinates1) and coordinates1[i] == coordinates1[i + 1]:
                    extrude_zahl += 1
                    i += 1
                    var += 1

                #collection and array reset
                for item in collections:
                    item.Delete()
                collections.Clear()
                tgcordinates.clear()

                #extrusion
                profile1 = sketch.Profiles.AddForSolid()
                extrude_feat = invPartDoc.ComponentDefinition.Features.ExtrudeFeatures
                extrude_def = extrude_feat.CreateExtrudeDefinition(profile1, wc.constants.kJoinOperation)
                extrude_def.SetDistanceExtent(extrude_distance * extrude_zahl, 20993)
                extrude_feat.Add(extrude_def)

                #variables for extrusion
                i -= var
                i += extrude_zahl


        except Exception as e:


            print(f"An error occurred: {e}")


    def top(coordinates2):


        # which layer are we on
        i = 0
        # how many times extrusion will be done
        extrude_zahl = 1

        #surface selection for drawing
        ksketch = invPartDoc.ComponentDefinition.Sketches.Add(xyPlane)


        while i < len(coordinates2):
            # temporary variables for layer control
            var = 0
            start = True

            #layer generation
            if i > 0:
                plane1 = invPartDoc.ComponentDefinition.WorkPlanes.AddByPlaneAndOffset(ksketch, extrude_distance * extrude_zahl, True)
                ksketch = invPartDoc.ComponentDefinition.Sketches.Add(plane1)
                extrude_zahl = 1

            #draw
            for j in range(len(coordinates2[i])):
                if coordinates2[i][j][0] == None:
                    for k in range(len(tgcordinates) - 1):
                        line1 = ksketch.SketchLines.AddByTwoPoints(tgcordinates[k], tgcordinates[k + 1])
                        collections.Add(line1)
                    tgcordinates.clear()
                    continue
                else:
                    if ((coordinates2[i][0][0] == coordinates2[i][j][0]) and (
                            coordinates2[i][0][1] == coordinates2[i][j][1]) and start == False):
                        line1 = ksketch.SketchLines.AddByTwoPoints(tgcordinates[j - 1], tgcordinates[0])
                        collections.Add(line1)
                    else:
                        tgcordinates.append(
                            ksketch.SketchPoints.Add(tg.CreatePoint2d(coordinates2[i][j][0], coordinates2[i][j][1])))
                        start = False

            #offset
            for j in range(len(tgcordinates) - 1):
                line1 = ksketch.SketchLines.AddByTwoPoints(tgcordinates[j], tgcordinates[j + 1])
                collections.Add(line1)
            ksketch.OffsetSketchEntitiesUsingDistance(collections, offset_distance, True)
            ksketch.OffsetSketchEntitiesUsingDistance(collections, offset_distance, False)

            #layer similarity check
            while i + 1 < len(coordinates2) and coordinates2[i] == coordinates2[i + 1]:
                extrude_zahl += 1
                var += 1
                i += 1

            # collection and array reset
            for item in collections:
                item.Delete()
            collections.Clear()
            tgcordinates.clear()

            #extrusion
            profile1 = ksketch.Profiles.AddForSolid()
            extrude_feat = invPartDoc.ComponentDefinition.Features.ExtrudeFeatures
            extrude_def = extrude_feat.CreateExtrudeDefinition(profile1, wc.constants.kJoinOperation)
            extrude_def.SetDistanceExtent(extrude_distance * extrude_zahl, 20993)
            try:
                extrude_feat.Add(extrude_def)
            except Exception as e:

                print(f"An error occurred: {e}")

            #variables for extrusion
            i -= var
            i += extrude_zahl

    def fill(coordinates3):

        # variables needed for extrusion
        sketch_counter = 0
        offset = True

        # surface selection for drawing
        osketch = invPartDoc.ComponentDefinition.Sketches.Add(xyPlane)

        # to hold temporary values
        dummy = []

        # if our drawing does not start from the first layer
        if coordinates3[0] == []:

            for i in range(len(coordinates3)):

                if coordinates3[i] == []:
                    if offset == True:
                        sketch_counter += 1
                else:
                    offset = False
                    dummy.append(coordinates3[i])
            if dummy != []:
                coordinates3 = dummy

        # layer adjustments
        if sketch_counter > 0:

            plane = invPartDoc.ComponentDefinition.WorkPlanes.AddByPlaneAndOffset(osketch,
                                                                                  extrude_distance * sketch_counter,
                                                                                  True)
            osketch = invPartDoc.ComponentDefinition.Sketches.Add(plane)



        # which layer are we on
        i = 0
        # how many times extrusion will be done
        extrude_zahl = 1


        while i < len(coordinates3):
            # temporary variables for layer control
            var = 0


            # layer generation
            if i > 0:
                plane2 = invPartDoc.ComponentDefinition.WorkPlanes.AddByPlaneAndOffset(osketch, extrude_distance * extrude_zahl, True)
                osketch = invPartDoc.ComponentDefinition.Sketches.Add(plane2)
                extrude_zahl = 1

            #draw
            for j in range(len(coordinates3[i])):
                if coordinates3[i][j][0] == None:
                    for k in range(len(tgcordinates) - 1):
                        osketch.AddStraightSlotByCenterToCenter(tgcordinates[k], tgcordinates[k + 1], 0.44/10)
                    tgcordinates.clear()
                    continue
                else:
                    tgcordinates.append(
                        osketch.SketchPoints.Add(tg.CreatePoint2d(coordinates3[i][j][0], coordinates3[i][j][1])))
            for j in range(len(tgcordinates) - 1):
                osketch.AddStraightSlotByCenterToCenter(tgcordinates[j], tgcordinates[j + 1], 0.44/10)

            # layer similarity check
            while i + 1 < len(coordinates3) and coordinates3[i] == coordinates3[i + 1]:
                extrude_zahl += 1
                i += 1
                var += 1
            # collection and array reset
            tgcordinates.clear()

            # extrusion
            profile1 = osketch.Profiles.AddForSolid()
            extrude_feat = invPartDoc.ComponentDefinition.Features.ExtrudeFeatures
            extrude_def = extrude_feat.CreateExtrudeDefinition(profile1, wc.constants.kJoinOperation)
            extrude_def.SetDistanceExtent(extrude_distance * extrude_zahl, 20993)
            extrude_feat.Add(extrude_def)

            #variables for extrusion
            i -= var
            i += extrude_zahl


    #for the first type
    if str(tail).startswith("A"):
        collections1, collections2, collections3 = give_array(filename)
        down(collections1)
        top(collections2)
        fill(collections3)

    #for the second type
    else:
        collections1, collections2, collections3, collections4, collections5, collections6, collections7, collections8, collections9 = give_array2(filename)
        top(collections1)
        down(collections2)
        down(collections3)
        down(collections4)
        down(collections5)
        down(collections6)
        down(collections7)
        fill(collections8)
        fill(collections9)

    #set view
    invApp.ActiveView.GoHome()






# -*- coding: utf-8 -*-
import arcpy


STYLES = {
    "Šauras līnijas mēroglineāls": "Scale Line 1 Metric",
    "Platas līnijas mēroglineāls": "Alternating Scale Bar 1 Metric",
}

# Iedaļas vērtība, Esri lineārās mērvienības kods un uzraksts.
DIVISIONS = {
    "100 metri": (100, 9001, "metri"),
    "1 kilometrs": (1, 9036, "kilometri"),
    "5 kilometri": (5, 9036, "kilometri"),
    "10 kilometri": (10, 9036, "kilometri"),
}

UNITS_PER_CM = {
    "CENTIMETER": 1,
    "MILLIMETER": 10,
    "INCH": 1 / 2.54,
    "POINT": 72 / 2.54,
}


class Toolbox:
    def __init__(self):
        self.label = "Mēroglineāli"
        self.alias = "meroglineali"
        self.tools = [InsertScaleBar]


class InsertScaleBar:
    def __init__(self):
        self.label = "Ievietot mēroglineālu"
        self.description = "Ievieto aktīvajā izkārtojumā ar karti saistītu mēroglineālu."
        self.canRunInBackground = False

    def getParameterInfo(self):
        style = arcpy.Parameter(
            displayName="Mēroglineāla veids",
            name="style",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        style.filter.type = "ValueList"
        style.filter.list = list(STYLES)
        style.value = "Šauras līnijas mēroglineāls"

        division = arcpy.Parameter(
            displayName="Mēroglineāla iedaļas vērtība",
            name="division",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        division.filter.type = "ValueList"
        division.filter.list = list(DIVISIONS)
        division.value = "1 kilometrs"
        return [style, division]

    def execute(self, parameters, messages):
        project = arcpy.mp.ArcGISProject("CURRENT")
        layout = project.activeView
        if not isinstance(layout, arcpy.mp.Layout):
            arcpy.AddError("Aktivizējiet izkārtojuma (Layout) cilni un palaidiet rīku vēlreiz.")
            raise arcpy.ExecuteError

        frames = [
            frame for frame in layout.listElements("MAPFRAME_ELEMENT")
            if frame.map is not None and frame.map.mapType == "MAP"
        ]
        if not frames:
            arcpy.AddError("Izkārtojumā nepieciešams kartes rāmis ar 2D karti.")
            raise arcpy.ExecuteError

        # Ja ir vairāki 2D rāmji, par galveno uzskata lielāko.
        frame = max(frames, key=lambda item: item.elementWidth * item.elementHeight)
        style_name = STYLES[parameters[0].valueAsText]
        styles = project.listStyleItems("ArcGIS 2D", "SCALE_BAR", style_name)
        style = next((item for item in styles if item.name == style_name), None)
        if style is None:
            arcpy.AddError(f'ArcGIS 2D stilos neizdevās atrast “{style_name}”.')
            raise arcpy.ExecuteError

        unit = UNITS_PER_CM[layout.pageUnits.upper().rstrip("S")]
        margin = min(unit, layout.pageWidth / 20, layout.pageHeight / 20)
        width = min(15 * unit, layout.pageWidth - 2 * margin)
        height = min(unit, layout.pageHeight - 2 * margin)
        bounds = arcpy.Polygon(arcpy.Array([
            arcpy.Point(margin, margin),
            arcpy.Point(margin, margin + height),
            arcpy.Point(margin + width, margin + height),
            arcpy.Point(margin + width, margin),
        ]))

        name = "Mēroglineāls"
        existing_names = {element.name for element in layout.listElements()}
        suffix = 2
        while name in existing_names:
            name = f"Mēroglineāls {suffix}"
            suffix += 1

        scale_bar = layout.createMapSurroundElement(bounds, "SCALE_BAR", frame, style, name)
        try:
            definition = layout.getDefinition("V3")
            bar = next(element for element in definition.elements if element.name == scale_bar.name)
            division, unit_code, unit_label = DIVISIONS[parameters[1].valueAsText]
            bar.units = {"uwkid": unit_code}
            bar.unitLabel = unit_label
            bar.unitLabelPosition = "AfterBar"
            bar.fittingStrategy = "AdjustDivisions"
            bar.division = division
            bar.subdivisions = 2

            create_cim = arcpy.cim.CreateCIMObjectFromClassName
            white = create_cim("CIMRGBColor", "V3")
            white.values = [255, 255, 255, 100]
            fill = create_cim("CIMSolidFill", "V3")
            fill.enable = True
            fill.color = white
            polygon = create_cim("CIMPolygonSymbol", "V3")
            polygon.symbolLayers = [fill]
            background = create_cim("CIMSymbolReference", "V3")
            background.symbol = polygon
            if bar.graphicFrame is None:
                bar.graphicFrame = create_cim("CIMGraphicFrame", "V3")
            bar.graphicFrame.backgroundSymbol = background
            layout.setDefinition(definition)
        except Exception:
            layout.deleteElement(scale_bar)
            raise

        arcpy.AddMessage(f'“{name}” ievietots izkārtojumā “{layout.name}” un piesaistīts rāmim “{frame.name}”.')

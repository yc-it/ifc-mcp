import ifcopenshell
from ifcopenshell import entity_instance


ifc = ifcopenshell.open(f"E:/temp01/1#综合楼-F1.ifc")
entity = ifc.by_id(357)
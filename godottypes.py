from dumper import *
import struct

# Variant types
VARIANT_TYPE_NIL,\
VARIANT_TYPE_BOOL,\
VARIANT_TYPE_INT,\
VARIANT_TYPE_REAL,\
VARIANT_TYPE_STRING,\
VARIANT_TYPE_VECTOR2,\
VARIANT_TYPE_RECT2,\
VARIANT_TYPE_VECTOR3,\
VARIANT_TYPE_TRANSFORM2D,\
VARIANT_TYPE_PLANE,\
VARIANT_TYPE_QUAT,\
VARIANT_TYPE_AABB,\
VARIANT_TYPE_BASIS,\
VARIANT_TYPE_TRANSFORM,\
VARIANT_TYPE_COLOR,\
VARIANT_TYPE_NODE_PATH,\
VARIANT_TYPE_RID,\
VARIANT_TYPE_OBJECT,\
VARIANT_TYPE_DICTIONARY,\
VARIANT_TYPE_ARRAY,\
VARIANT_TYPE_POOL_BYTE_ARRAY,\
VARIANT_TYPE_POOL_INT_ARRAY,\
VARIANT_TYPE_POOL_REAL_ARRAY,\
VARIANT_TYPE_POOL_STRING_ARRAY,\
VARIANT_TYPE_POOL_VECTOR2_ARRAY,\
VARIANT_TYPE_POOL_VECTOR3_ARRAY,\
VARIANT_TYPE_POOL_COLOR_ARRAY,\
VARIANT_TYPE_VARIANT_MAX, \
 = range(0,  28)

VARIANT_NAMES = [
	"Nil",
	"bool",
	"int",
	"float",
	"String",

	"Vector2",
	"Rect2",
	"Vector3",
	"Transform2D",
	"Plane",
	"Quat",
	"AABB",
	"Basis",
	"Transform",
	"Color",
	"NodePath",
	"RID",
	"Object",
	"Dictionary",
	"Array",

	"PoolByteArray",
	"PoolIntArray",
	"PoolRealArray",
	"PoolStringArray",
	"PoolVector2Array",
	"PoolVector3Array",
	"PoolColorArray",
	"InvalidVariant",
]

def extract_bytes(dumper, addr, size):
	result = bytearray()
	end_pos = addr + size
	while True:
		d = dumper.extractByte(addr)
		addr += 1
		if addr > end_pos:
			break
		result.append(d)
	return result

def qdump__Variant(d, value):
	type = value['type'].integer()
	mem = value['_data']
	ptr = value['_data']['_ptr']
	content = get_variant_title(type, mem)
	if len(content):
		d.putValue('[{}] {}'.format(VARIANT_NAMES[type], content))
	elif type == VARIANT_TYPE_STRING:
		d.putItem(mem.cast('wchar_t*'))
		d.putType(value.type)
	elif type == VARIANT_TYPE_OBJECT:
		d.putValue("[Object] 0x%x" % ptr.pointer())
		d.putType(value.type)
	d.putNumChild(2)
	if d.isExpanded():
		with Children(d):
			if type == VARIANT_TYPE_OBJECT: d.putSubItem("ptr", ptr.cast('%s*' % VARIANT_NAMES[type]))
			d.putFields(value)

def qdump__Vector2(d, value):
	d.putNumChild(2)
	d.putValue(get_variant_title(VARIANT_TYPE_VECTOR2, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Vector3(d, value):
	d.putNumChild(3)
	d.putValue(get_variant_title(VARIANT_TYPE_VECTOR3, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Color(d, value):
	d.putNumChild(4)
	d.putValue(get_variant_title(VARIANT_TYPE_COLOR, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Rect2(d, value):
	d.putNumChild(2)
	d.putValue(get_variant_title(VARIANT_TYPE_RECT2, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Quat(d, value):
	d.putNumChild(4)
	d.putValue(get_variant_title(VARIANT_TYPE_QUAT, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Transform2D(d, value):
	d.putNumChild(1)
	d.putValue(get_variant_title(VARIANT_TYPE_TRANSFORM2D, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Basis(d, value):
	d.putNumChild(1)
	d.putValue(get_variant_title(VARIANT_TYPE_BASIS, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Transform(d, value):
	d.putNumChild(2)
	d.putValue(get_variant_title(VARIANT_TYPE_TRANSFORM, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__AABB(d, value):
	d.putNumChild(2)
	d.putValue(get_variant_title(VARIANT_TYPE_AABB, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)
			
def qdump__Plane(d, value):
	d.putNumChild(2)
	d.putValue(get_variant_title(VARIANT_TYPE_PLANE, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__RID(d, value):
	d.putNumChild(1)
	d.putValue(get_variant_title(VARIANT_TYPE_RID, value))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def get_variant_title(type, mem):
	content = ""
	if type == VARIANT_TYPE_NIL: content = "null"
	elif type == VARIANT_TYPE_INT: content = str(mem.integer())
	elif type == VARIANT_TYPE_BOOL: content = str(mem.bool())
	elif type == VARIANT_TYPE_REAL: content = str(mem.floatingPoint())
	elif type == VARIANT_TYPE_RID: content = str(mem.extractInteger(32, True))
	elif type in [VARIANT_TYPE_COLOR, VARIANT_TYPE_RECT2, VARIANT_TYPE_QUAT]: content = '(%s, %s, %s, %s)' % (mem.split('ffff'))
	elif type == VARIANT_TYPE_VECTOR2: content = '(%s, %s)' % (mem.split('ff'))
	elif type == VARIANT_TYPE_VECTOR3: content = '(%s, %s, %s)' % (mem.split('fff'))
	elif type == VARIANT_TYPE_TRANSFORM2D: content = '[(%s, %s), (%s, %s), (%s, %s)]' % (mem.split('ffffff'))
	elif type == VARIANT_TYPE_AABB: content = '[(%s, %s, %s), (%s, %s, %s)]' % (mem.split('ffffff'))
	elif type == VARIANT_TYPE_BASIS: content = '[(%s, %s, %s), (%s, %s, %s), (%s, %s, %s)]' % (mem.split('fffffffff'))
	elif type == VARIANT_TYPE_TRANSFORM: content = '[[(%s, %s, %s), (%s, %s, %s), (%s, %s, %s)], (%s, %s, %s)]' % (mem.split('ffffffffffff'))
	elif type == VARIANT_TYPE_PLANE: content = '[(%s, %s, %s), %s]' % (mem.split('ffff'))
	return content

def qdump__String(d, value):
	if value["_cowdata"]["_ptr"].integer() == 0:
		d.putValue('<empty>')
		return
	d.putItem(value["_cowdata"]["_ptr"])
	d.putType(value.type)
	d.putNumChild(2)
	if d.isExpanded():
		with Children(d):
			if d.canCallLocale():
				d.putCallItem('length', 'int', value, 'length')
			d.putFields(value)

def qdump__StringName(d, value):
	cname = value["_data"]["cname"]
	item = cname
	if cname.integer() == 0:
		name = value["_data"]["name"]
		item = name["_cowdata"]["_ptr"]
	d.putItem(item)
	d.putType(value.type)
	d.putNumChild(1)
	if d.isExpanded():
		with Children(d):
			d.putFields(value)


def qdump__Vector(d, value):
	ptr = value["_cowdata"]["_ptr"]
	if ptr.pointer() == 0:
		d.putValue("<empty>")
		return
	size = d.parseAndEvaluate("size()").integer()
	type = d.templateArgument(value.type, 0)
	d.putValue("0x%x [size %i]" % (value.laddress, size))
	d.putNumChild(size)
	if d.isExpanded():
		d.putArrayData(ptr.pointer(), size, type)
		
def qdump__Array(d, value):
	size = d.parseAndEvaluate("size();").integer()
	if size == 0:
		d.putValue("<empty>")
		return
	d.putValue("0x%x [size %i]" % (value.laddress, size))
	d.putNumChild(size)
	if d.isExpanded():
		arr = value['_p']["array"]
		d.putArrayData(arr.address(), size, d.lookupType("Variant"))

def qdump__Vector2i(d, value):
	d.putNumChild(2)
	d.putValue("(%i, %i)" % (value.split("ii")))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

def qdump__Rect2i(d, value):
	d.putNumChild(2)
	d.putValue("(%i, %i, %i, %i)" % (value.split("iiii")))
	if d.isExpanded():
		with Children(d):
			d.putFields(value)

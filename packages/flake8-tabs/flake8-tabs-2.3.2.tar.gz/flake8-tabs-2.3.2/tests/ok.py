import sys
import typing as ty


class ACtxManager:
	async def __aenter__(self):
		return 1
	
	async def __aexit__(self, *a):
		return False


def demo():
	"""Do something
	
	This code may be considered helpful::
	
		print(1, 2, 3)
	
	This line is dedented again.
	"""
	iter({
		"a": int("6",
		         10)
	})
	
	[
		"--arg1",
		"--arg2",
	] + sys.argv[1:]
	
	FAKE_FILE1_HASH = {"value1": "DATA",
	                   "Name": "fsdfgh", "Size": "16"}
	
	# Examples of backslash continuation lines (PEP-8 / “Maximum Line Length”)
	assert len(sys.argv) == 2, \
	       "Maybe pass more args? " \
	       "And more!?"
	assert not False, \
	       "This shouldn't align with “not”, but just “assert”"
	with open('/path/to/some/file/you/want/to/read') as file_1, \
	     open('/path/to/some/file/being/written', 'w') as file_2:
		file_2.write(file_1.read())
	async def wrapper():
		async with ACtxManager() as a, \
		           ACtxManager() as b:
			print(a + b)
	if len(sys.argv) == \
	   len(FAKE_FILE1_HASH) \
	   and file_1:
		pass
	
	def download(self, path, args=[], filepath=None, opts={},
	             compress=True, **kwargs):
		return path is not None \
		       or len(args) >= 1
	
	return (
		("bla", FAKE_FILE1_HASH
	))


def foobar(  # A comment here should not cause error ET128
		arg1,
		arg2
):
	pass

def foobar2(arg1,
            arg2):
	pass

# Useless list containing mixed start-of-line and end-of-line brackets
[
	(
		1,
		2,
		3,
	), (
		4,
		5,
		6,
	)
]

# Test for GL/ntninja/flake8-tabs#3: Multiline bracketed return types
def test_return_tuple(
		isTrue: bool,
		value: ty.Any
) -> ty.Tuple[
		bool,  # A note here
		ty.Optional[ty.Any]  # Another note here
]:
	return True, 5

some = super = deep = call = print

# I sure hope nobody ever does the following
some(super(deep(call(
	"with"),
	"several"),
	"arguments"),
	lambda x: x)

# Sadly this triggers the same code but is very different
print(sum([
	1,
	2,
	3,
]), end="\n\n")
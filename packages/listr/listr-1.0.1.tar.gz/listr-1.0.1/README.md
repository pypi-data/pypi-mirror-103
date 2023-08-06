 **Listr**  is python module that can be used to:
- iterate list through pointer/cursor  `current()`,  `next()` ,  `prev()` ,   `start()` ,  `end()`.
- iterate list through  `iter()` (without looping/queue-like)

### installation
```
pip install listr
```

### Example
```python
# -*- coding: utf-8 -*-
from listr import Listr
import unittest

class ListrTest(unittest.TestCase):

	def test_pointer(self):
		t = Listr()
		t.import_list(["one","two","three"])
		self.assertEqual(t.current(), "one")
		self.assertEqual(t.next(), "two")
		self.assertEqual(t.next(), "three")
		self.assertEqual(t.next(), "one")
		self.assertEqual(t.prev(), "three")
		self.assertEqual(t.start(), "one")
		self.assertEqual(t.end(), "three")

	def test_iterator(self):
		t = Listr()
		t.import_list(range(1,10))
		for i in t.list:
			self.assertEqual(i,t.iter())
		self.assertEqual(t.iter_check(), False)
		t.iter_reset()
		self.assertEqual(t.iter_num, 0)


if __name__=="__main__":
	unittest.main()
	

```

### Hint
- you can access list through  `Listr.list` property/attribute.
-  `iter()` can be access with python native iterator (Listr object is iterable).
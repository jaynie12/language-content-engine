import sys
if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
   print("Inside a virtual environment")
else:
   print("Not in a virtual environment")
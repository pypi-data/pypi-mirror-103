#!/usr/bin/env python3

class CLException(Exception) : pass
class CLExitException(CLException) : pass
class CLInterruptException(CLException) : pass


"""Custom exceptions."""

class ZKForgeError(Exception): pass
class ProofError(ZKForgeError): pass
class VerifyError(ZKForgeError): pass
class FieldError(ZKForgeError): pass
class GPUError(ZKForgeError): pass

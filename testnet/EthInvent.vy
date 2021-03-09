# @author ausernamewastaken

currentSubmissionCount: public(uint256)
countToSubmission: HashMap[uint256, bytes32]

event HashSubmitted:
    submissionCount: uint256
    hashOfContent: bytes32

@external
def __init__():
    self.currentSubmissionCount = 0

@external
def submitHash(_hashOfContent: bytes32) -> bool:
    self.countToSubmission[self.currentSubmissionCount] = _hashOfContent
    log HashSubmitted(self.currentSubmissionCount, _hashOfContent)
    
    self.currentSubmissionCount += 1
    return True
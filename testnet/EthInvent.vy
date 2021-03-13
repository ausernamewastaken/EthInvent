# @author ausernamewastaken

submissions: public(HashMap[bytes32, uint256])

event HashSubmitted:
    hashOfContent: bytes32

@external
def submitHash(_hashOfContent: bytes32) -> bool:

    assert self.submissions[_hashOfContent] == 0

    self.submissions[_hashOfContent] = block.timestamp

    log HashSubmitted(_hashOfContent)
    
    return True
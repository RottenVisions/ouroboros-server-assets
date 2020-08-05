import math
import Math

def brokenDONTUSE(caster, target, fov):
    """
	Whether the entity is in the fan range
	"""
    srcPos = Math.Vector3(caster.position)
    srcPos.y = 0

    desPos = Math.Vector3(target.position)
    desPos.y = 0

    desDir = desPos - srcPos
    desDir.y = 0
    desDir.normalise()

    yawRadians = caster.direction.z
    yaw = math.degrees(yawRadians)
    facingDir = Math.Vector3(0, 0, yaw)
    an = facingDir.dot(desDir)

    if an < -1:
        an = -1

    if an == 0:  # Just in the same position as the caster
        an = 1

    if an > 1:
        an = 1

    angle = int(math.acos(an) / 3.1415926 * 180)
    if angle <= fov / 2:  # Less than or equal to the angle
        return True

    return False

def inFieldOfView2(caster, target, fov):
    srcPos = Math.Vector3(caster.position)
    #srcPos.y = 0

    desPos = Math.Vector3(target.position)
    #desPos.y = 0

    desDir = desPos - srcPos
    #desDir.y = 0
    #desDir.normalise()

    yawRadians = caster.direction.z
    yaw = math.degrees(yawRadians)
    facingDir = Math.Vector3(0, yaw, 0)
    #facingDir.normalise()
    print('cast dir: ', caster.direction)
    print('src pos: ', srcPos)
    print('dest pos: ', desPos)
    print('b4 norm', desPos - srcPos)
    print('facing: ', facingDir)
    print('dest: ', desDir)
    print('dest: ', desDir)

    foundAngle = angle(desDir, facingDir)
    print('found this angle', foundAngle)
    if foundAngle < fov / 2:
        return True
    return False

def inFieldOfView(caster, target, fov, showDebug = False):
    srcPos = Math.Vector3(caster.position)
    desPos = Math.Vector3(target.position)
    halfFov = fov / 2

    desDir = desPos - srcPos
    angleRadians = math.atan2(desDir.x, desDir.z)
    angleRelativeToSource = math.degrees(angleRadians)

    newAngleSource = angleRelativeToSource

    yawRadians = caster.direction.z
    yawUnwrapped = math.degrees(yawRadians)
    yaw = yawUnwrapped

    # Wrap angle (normally goes 0 - 180, then -180 - 0
    if yawUnwrapped < 0:
        yaw = yawUnwrapped + 360

    # More angle wrapping
    if angleRelativeToSource < 0:
        newAngleSource = 360 + angleRelativeToSource
    else:
        newAngleSource = angleRelativeToSource

    if (newAngleSource + halfFov) >= 360:
        rhs = (newAngleSource + halfFov) - 360
    else:
        rhs = newAngleSource + halfFov

    if (newAngleSource - halfFov) < 0:
        subtractFrom = abs(newAngleSource - halfFov)
        lhs = 360 - subtractFrom
    else:
        lhs = newAngleSource - halfFov

    solved = False
    if lhs > rhs:
        aboveLhs = yaw >= lhs and yaw <= 360
        belowRhs = yaw >= 0 and yaw <= rhs
        if aboveLhs or belowRhs:
            solved = True
    else:
        aboveLhs = yaw >= lhs
        belowRhs = yaw <= rhs
        if aboveLhs and belowRhs:
            solved = True

    if showDebug:
        print('ang rel to src: ', angleRelativeToSource)
        print('new angleSrc: ', newAngleSource)
        print('yaw: ', yaw)
        print('half fov: ', halfFov)
        print('lhs: ', lhs)
        print('rhs: ', rhs)
        print('above lhs: ', aboveLhs)
        print('below rhs: ', belowRhs)

    if solved:
        return True
    else:
        return False

def angle(fromVec, toVec):
    fromVecSqr = sqrMagnitude(fromVec)
    toVecSqr = sqrMagnitude(toVec)
    num = math.sqrt(fromVecSqr * toVecSqr)
    result = 0.0
    if num < 0.00000000000000100000000362749:
        result = 0.0
    else:
        an = fromVec.dot(toVec)
        ann = clamp((an / num), -1, 1)
        result = math.acos(ann) * 57.29578
    return result


def sqrMagnitude(vec):
    return (vec.x * vec.x) + (vec.y * vec.y) + (vec.z * vec.z)

def clamp(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max
    return value

def wrapAngle(angle):
    angle %= 360
    if angle > 180:
        return angle - 360
    return angle

def unwrapAngle(angle):
    if angle >= 0:
        return angle
    angle = -angle%360
    return 360 - angle
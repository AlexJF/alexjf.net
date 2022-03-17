const frustumSize = 100;
const boxSize = 10;
// lets add an extra set of boxes around determined box field to account for perspective "holes"
const margin = -boxSize;
let updated = true;

const pointerVector = new THREE.Vector2();
const positionVector = new THREE.Vector3();
const instanceMatrix4 = new THREE.Matrix4();
const transformationMatrix4 = new THREE.Matrix4();

const pressAnimationSpeed = 0.5;
const releaseAnimationSpeed = 0.5;
const animationDisplacement = boxSize;
const pressureDistance = 4 * boxSize;

// https://easings.net/#easeInCubic
function easeInCubic(x) {
    return x * x * x;
}

class Box {
    constructor(instancedMesh, index, position, size) {
        this.instancedMesh = instancedMesh;
        this.index = index;
        this.size = size || 1;
        this.stablePosition = position;
        this.displacementPosition = position.clone();
        this.displacementPosition.z -= animationDisplacement;
        this.displacementProgress = 0;
        this.pressed = false;
        this.pressure = 0;
        this._updateMesh(instanceMatrix4.identity());
        this.scale(size, size, size);
        this.move(position.x, position.y, position.z);
    }

    getIndex() {
        return this.index;
    }

    getPosition() {
        positionVector.setFromMatrixPosition(this._getMatrix());
        return positionVector;
    }

    setPosition(x, y, z) {
        const matrix = this._getMatrix();
        matrix.setPosition(x, y, z);
        this._updateMesh(matrix);
    }

    setPressure(pressure) {
        this.pressure = pressure;
    }

    distanceTo(otherBox) {
        return this.getPosition().clone().sub(otherBox.getPosition()).length();
    }

    move(dx, dy, dz) {
        const translateMatrix = transformationMatrix4;
        translateMatrix.makeTranslation(dx, dy, dz);
        const matrix = this._getMatrix();
        matrix.premultiply(translateMatrix);
        this._updateMesh(matrix);
    }

    scale(dx, dy, dz) {
        const scalingMatrix = transformationMatrix4;
        const matrix = this._getMatrix();
        scalingMatrix.makeScale(dx, dy, dz);
        matrix.premultiply(scalingMatrix);
        this._updateMesh(matrix);
    }

    update(elapsedMillis) {
        let easingFunction = easeInCubic;
        if (this.displacementProgress === this.pressure) {
            return false;
        }
        const pressed = this.displacementProgress <= this.pressure && this.pressure > 0;
        if (pressed) {
            //easingFunction = easeInExpo;
            this.displacementProgress = Math.min(this.pressure, this.displacementProgress + elapsedMillis / 1000 * pressAnimationSpeed);
        } else {
            this.displacementProgress = Math.max(this.pressure, this.displacementProgress - elapsedMillis / 1000 * releaseAnimationSpeed);
        }
        const movementVector = this.stablePosition.clone().sub(this.displacementPosition);
        const multiplier = easingFunction(1 - this.displacementProgress);
        const targetPosition = movementVector.multiplyScalar(multiplier).add(this.displacementPosition);
        this.setPosition(targetPosition.x,targetPosition.y, targetPosition.z);

        return true;
    }

    _getMatrix() {
        this.instancedMesh.getMatrixAt(this.index, instanceMatrix4);
        return instanceMatrix4;
    }

    _updateMesh(matrix) {
        this.instancedMesh.setMatrixAt(this.index, matrix);
        this.instancedMesh.instanceMatrix.needsUpdate = true;
    }
}

const canvas = document.querySelector('canvas.background');
const scene = new THREE.Scene();
scene.background = new THREE.Color('#434c5e');
const camera = new THREE.OrthographicCamera();
const renderer = new THREE.WebGLRenderer({canvas});
let boxes = [];

const material1 = new THREE.MeshBasicMaterial( { color: '#434c5e' } );
const material2 = new THREE.MeshBasicMaterial( { color: '#3b4252' } );
const material3 = new THREE.MeshBasicMaterial( { color: '#4c566a' } );
const geometry = new THREE.BoxGeometry(1, 1, 1);
const materials = [
    material2, // px
    material3, // nx
    material3, // py
    material2, // ny
    material1, // pz
    material1, // nz
]

let boxInstancedMesh = new THREE.InstancedMesh(geometry, materials, 1);

const cameraCorners = [
    new THREE.Vector3(-1, -1, 0),
    new THREE.Vector3(1, -1, 0),
    new THREE.Vector3(1, 1, 0),
    new THREE.Vector3(-1, 1, 0),
]

function setup() {
    const aspectRatio = window.innerWidth / window.innerHeight;
    const frustumWidth = frustumSize * aspectRatio;
    const frustumHeight = frustumSize;
    camera.near = 0;
    camera.far = 1000;
    camera.top = frustumHeight / 2;
    camera.bottom = -frustumHeight / 2;
    camera.left = -frustumWidth / 2;
    camera.right = frustumWidth / 2;
    camera.position.set(frustumHeight / 2, frustumHeight / 2, frustumHeight / 2);
    // I prefer x and y as a horizontal plane and z as the "height" component
    camera.up.set(0, 0, 1);
    camera.lookAt(0, 0, 0);
    camera.updateMatrix();
    camera.updateMatrixWorld();
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight, false);

    scene.clear();

    const cornerWorldPos = cameraCorners
        .map(p => unprojectToZPlane(p, camera, 0));
    let minX = +Infinity;
    let minY = +Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    cornerWorldPos.forEach(p => {
        minX = Math.min(minX, p.x);
        maxX = Math.max(maxX, p.x);
        minY = Math.min(minY, p.y);
        maxY = Math.max(maxY, p.y);
    })
    minX += margin;
    minY += margin;
    maxX -= margin;
    maxY -= margin;

    const floorWidth = maxX - minX;
    const floorHeight = maxY - minY;

    const numRows = Math.ceil(floorHeight / boxSize);
    const numColumns = Math.ceil(floorWidth / boxSize);
    boxes = [];
    boxInstancedMesh.dispose();
    boxInstancedMesh = new THREE.InstancedMesh(geometry, materials, numRows * numColumns);
    scene.add(boxInstancedMesh);
    for (let r = 0; r < numRows; r++) {
        const y = minY + r * boxSize;
        for (let c = 0; c < numColumns; c++) {
            const x = minX + c * boxSize;
            const position = new THREE.Vector3(x, y, 0);
            const i = numColumns * r + c;
            const b = new Box(boxInstancedMesh, i, position, boxSize)
            boxes.push(b);
        }
    }
    updated = true;
}

function unprojectToZPlane(position, camera, z) {
    if (camera instanceof THREE.PerspectiveCamera) {
        return unprojectToZPlanePerspective(position, camera, z);
    }
    else if (camera instanceof THREE.OrthographicCamera) {
        return unprojectToZPlaneOrtho(position, camera, z);
    }
    else {
        throw new Error("unknown camera");
    }
}

function unprojectToZPlanePerspective(position, camera, z) {
    // if no z specified, assume 0
    const targetZ = z || 0;
    // lets unproject the camera position
    const vec = position.clone().unproject(camera);
    // then get a normalized vector with the raycasting direction
    vec.sub(camera.position).normalize();
    // Project onto chosen z by calculating scaling factor to chosen z and then subtracting from camera
    const distance = (targetZ - camera.position.z) / vec.z;
    return camera.position.clone().add(vec.multiplyScalar(distance));
}

function unprojectToZPlaneOrtho(position, camera, z) {
    // if no z specified, assume 0
    const targetZ = z || 0;
    // lets unproject the camera position
    const vec = position.clone().unproject(camera);
    // then get a normalized vector with the raycasting direction
    const cameraDirection = new THREE.Vector3();
    camera.getWorldDirection(cameraDirection);
    cameraDirection.normalize();
    // Project onto chosen z by calculating scaling factor to chosen z and then subtracting from camera
    const distance = (targetZ - vec.z) / cameraDirection.z;
    return vec.add(cameraDirection.multiplyScalar(distance));
}

let t = null;
window.onresize =function() {
    if (t!= null) clearTimeout(t);

    t = setTimeout(function() {
        // work around quirky handling of 100vh specially on ios
        document.body.style.minHeight = `${Math.floor(window.innerHeight) - 1}px`;
        setup();
    }, 500);
};
window.onresize(null);

let lastAnimateTimestamp = undefined;
function animate(timestamp) {
    if (lastAnimateTimestamp === undefined) {
        lastAnimateTimestamp = timestamp;
    }
    const elapsedMillis = timestamp - lastAnimateTimestamp;
    lastAnimateTimestamp = timestamp;
    requestAnimationFrame(animate);
    if (!updated) {
        return;
    }
    updated = boxes.reduce((updated, b) => b.update(elapsedMillis) || updated, false);
    renderer.render(scene, camera);
}
requestAnimationFrame(animate);

const raycaster = new THREE.Raycaster();
let pressedBoxes = new Set();

function onPointerMove( event ) {
    // calculate pointer position in normalized device coordinates
    // (-1 to +1) for both components
    pointerVector.x = (( event.clientX / window.innerWidth) * 2 - 1);
    pointerVector.y = (- ( event.clientY / window.innerHeight ) * 2 + 1);

    // update the picking ray with the camera and pointer position
    raycaster.setFromCamera( pointerVector, camera );

    const intersects = raycaster.intersectObject(boxInstancedMesh);

    let referenceBox = intersects.length > 0 ? boxes[intersects[0].instanceId] : undefined;

    const newPressedBoxes = new Set();
    if (referenceBox) {
        // press boxes near pointer
        for (let box of boxes) {
            const distanceToReference = referenceBox.distanceTo(box);
            const normalizedPressure = Math.max(0, 1 - distanceToReference / pressureDistance);
            box.setPressure(normalizedPressure);
            newPressedBoxes.add(box.getIndex());
        }
    }

    /*
    // press boxes that intersect with pointer
    const newPressedBoxes = new Set();
    for (let i = 0; i < intersects.length; i++) {
        newPressedBoxes.add(intersects[i].instanceId);
        boxes[intersects[i].instanceId].press();
    }
    */

    // release boxes that are no longer pressed
    for (let instanceId of pressedBoxes.values()) {
        if (!newPressedBoxes.has(instanceId)) {
            boxes[instanceId].setPressure(0);
        }
    }
    pressedBoxes = newPressedBoxes;

    updated = true;
}

function resetPressure() {
    // release boxes that are no longer pressed
    for (let instanceId of pressedBoxes.values()) {
        boxes[instanceId].setPressure(0);
    }
    pressedBoxes.clear();

    updated = true;
}

window.addEventListener('pointermove', onPointerMove)
window.addEventListener('pointerout', resetPressure)

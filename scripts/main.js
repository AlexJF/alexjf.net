const frustumSize = 100;
const boxSize = 10;

class Box {
    constructor(instancedMesh, index, position, size) {
        this.instancedMesh = instancedMesh;
        this.index = index;
        this.matrix = new THREE.Matrix4();
        this.size = size || 1;
        this.refPosition = position;
        this.scale(size, size, size);
        this.move(position.x, position.y, position.z);
    }

    getIndex() {
        return this.index;
    }

    getPosition() {
        const positionVector = new THREE.Vector3();
        positionVector.setFromMatrixPosition(this.matrix);
        return positionVector;
    }

    setPosition(x, y, z) {
        this.matrix.setPosition(x, y, z);
        this._updateMesh();
    }

    move(dx, dy, dz) {
        const translateMatrix = new THREE.Matrix4();
        translateMatrix.makeTranslation(dx, dy, dz);
        this.matrix.premultiply(translateMatrix);
        this._updateMesh();
    }

    scale(dx, dy, dz) {
        const scalingMatrix = new THREE.Matrix4();
        scalingMatrix.makeScale(dx, dy, dz);
        this.matrix.premultiply(scalingMatrix);
        this._updateMesh();
    }

    update() {
        const position = this.getPosition();
        const diff = position.z - this.refPosition.z;

        const magnitude = Math.min(Math.abs(diff), this.size / 100);

        if (diff > 0) {
            this.move(0, 0, -magnitude);
        } else if (diff < 0) {
            this.move(0,  0, magnitude);
        }
    }

    _updateMesh() {
        this.instancedMesh.setMatrixAt(this.index, this.matrix);
        this.instancedMesh.instanceMatrix.needsUpdate = true;
    }
}

const canvas = document.querySelector('canvas.background');
const scene = new THREE.Scene();
scene.background = new THREE.Color('#2e3440');
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

    const frustumScaler = new THREE.Matrix4();
    frustumScaler.makeScale(frustumWidth / 2, frustumHeight / 2, 0);
    const cornerWorldPos = cameraCorners
        .map(p => p.applyMatrix4(frustumScaler))
        .map(p => unprojectToZPlane(p, camera));
    console.log(cornerWorldPos);
    let minX = +Infinity;
    let minY = +Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    cornerWorldPos.forEach(p => {
        console.log(p);
        minX = Math.min(minX, p.x);
        maxX = Math.max(maxX, p.x);
        minY = Math.min(minY, p.y);
        maxY = Math.max(maxY, p.y);
    })
    console.log(`floor x = [${minX}, ${maxX}]`);
    console.log(`floor y = [${minY}, ${maxY}]`);

    const floorWidth = maxX - minX;
    const floorHeight = maxY - minY;

    const numRows = Math.ceil(floorHeight / boxSize);
    const numColumns = Math.ceil(floorWidth / boxSize);
    console.log(`Num rows = ${numRows}`);
    console.log(`Num columns = ${numColumns}`);
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
}

function unprojectToZPlane(position, camera, z) {
    // if no z specified, assume 0
    const targetZ = z || 0;
    // lets unproject the camera position
    const vec = position.clone().unproject(camera);
    // then normalized vector from camera position to projected position
    vec.sub(camera.position).normalize();
    // Project onto chosen z by calculating scaling factor to chosen z and then subtracting from camera
    const distance = (targetZ - camera.position.z) / vec.z;
    return camera.position.clone().add(vec.multiplyScalar(distance));
}

setup();

function animate() {
    requestAnimationFrame( animate );
    boxes.forEach(b => b.update());
    renderer.render( scene, camera );
}
animate();

window.onresize = setup;

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

function onPointerMove( event ) {
    // calculate pointer position in normalized device coordinates
    // (-1 to +1) for both components
    pointer.x = (( event.clientX / window.innerWidth) * 2 - 1);
    pointer.y = (- ( event.clientY / window.innerHeight ) * 2 + 1);

    // update the picking ray with the camera and pointer position
    raycaster.setFromCamera( pointer, camera );

    const intersects = raycaster.intersectObject(boxInstancedMesh);

    for ( let i = 0; i < intersects.length; i++ ) {
        boxes[intersects[i].instanceId].move(0, 0, -1);
    }
}

window.addEventListener('pointermove', onPointerMove)

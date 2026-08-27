/**
 * MediAI 2.0 — Interactive 3D WebGL Bio-Sphere & DNA Mesh Engine
 * Powered by Three.js
 */

(function () {
    const container = document.getElementById("threeCanvasContainer");
    if (!container || typeof THREE === "undefined") return;

    let scene, camera, renderer;
    let bioSphere, dnaGroup, particleCloud;
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;
    let windowHalfX = container.clientWidth / 2;
    let windowHalfY = container.clientHeight / 2;

    function init() {
        // 1. Scene Setup
        scene = new THREE.Scene();

        // 2. Camera Setup
        camera = new THREE.PerspectiveCamera(
            45,
            container.clientWidth / container.clientHeight,
            0.1,
            1000
        );
        camera.position.z = 26;

        // 3. Renderer Setup
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // 4. Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0x00f2fe, 2, 50);
        pointLight1.position.set(10, 10, 10);
        scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0x6366f1, 2, 50);
        pointLight2.position.set(-10, -10, 10);
        scene.add(pointLight2);

        // 5. Construct 3D Bio-Neural Sphere
        const sphereGeo = new THREE.IcosahedronGeometry(6.5, 2);
        const sphereMat = new THREE.MeshStandardMaterial({
            color: 0x00f2fe,
            wireframe: true,
            transparent: true,
            opacity: 0.35,
            roughness: 0.2,
            metalness: 0.8
        });
        bioSphere = new THREE.Mesh(sphereGeo, sphereMat);
        scene.add(bioSphere);

        // Inner Glowing Core Sphere
        const coreGeo = new THREE.SphereGeometry(3.2, 32, 32);
        const coreMat = new THREE.MeshBasicMaterial({
            color: 0x0284c7,
            wireframe: true,
            transparent: true,
            opacity: 0.25
        });
        const coreMesh = new THREE.Mesh(coreGeo, coreMat);
        bioSphere.add(coreMesh);

        // 6. Construct 3D DNA Double Helix Mesh
        dnaGroup = new THREE.Group();
        const dnaLength = 36;
        const strandRadius = 8.5;
        const spherePuckGeo = new THREE.SphereGeometry(0.24, 12, 12);
        const cyanMat = new THREE.MeshBasicMaterial({ color: 0x00f2fe });
        const purpleMat = new THREE.MeshBasicMaterial({ color: 0xa855f7 });
        const rungMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.25 });

        for (let i = 0; i < dnaLength; i++) {
            const angle = (i / dnaLength) * Math.PI * 4;
            const y = (i - dnaLength / 2) * 0.45;

            const x1 = Math.cos(angle) * strandRadius;
            const z1 = Math.sin(angle) * strandRadius;
            const puck1 = new THREE.Mesh(spherePuckGeo, cyanMat);
            puck1.position.set(x1, y, z1);
            dnaGroup.add(puck1);

            const x2 = Math.cos(angle + Math.PI) * strandRadius;
            const z2 = Math.sin(angle + Math.PI) * strandRadius;
            const puck2 = new THREE.Mesh(spherePuckGeo, purpleMat);
            puck2.position.set(x2, y, z2);
            dnaGroup.add(puck2);

            // Connective Base Pair Rung
            const points = [new THREE.Vector3(x1, y, z1), new THREE.Vector3(x2, y, z2)];
            const rungGeo = new THREE.BufferGeometry().setFromPoints(points);
            const rung = new THREE.Line(rungGeo, rungMat);
            dnaGroup.add(rung);
        }
        dnaGroup.rotation.z = Math.PI / 4;
        scene.add(dnaGroup);

        // 7. Ambient Particle Field Cloud
        const particleCount = 200;
        const particleGeo = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 40;
            positions[i + 1] = (Math.random() - 0.5) * 40;
            positions[i + 2] = (Math.random() - 0.5) * 40;
        }

        particleGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
        const particleMat = new THREE.PointsMaterial({
            color: 0x38bdf8,
            size: 0.15,
            transparent: true,
            opacity: 0.6
        });
        particleCloud = new THREE.Points(particleGeo, particleMat);
        scene.add(particleCloud);

        // 8. Event Listeners
        window.addEventListener("resize", onWindowResize);
        container.addEventListener("mousemove", onMouseMove);
        container.addEventListener("mouseleave", onMouseLeave);

        animate();
    }

    function onWindowResize() {
        if (!container) return;
        windowHalfX = container.clientWidth / 2;
        windowHalfY = container.clientHeight / 2;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function onMouseMove(event) {
        const rect = container.getBoundingClientRect();
        mouseX = (event.clientX - rect.left - windowHalfX) * 0.001;
        mouseY = (event.clientY - rect.top - windowHalfY) * 0.001;
    }

    function onMouseLeave() {
        mouseX = 0;
        mouseY = 0;
    }

    function animate() {
        requestAnimationFrame(animate);

        // Smooth Mouse Parallax
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        if (bioSphere) {
            bioSphere.rotation.y += 0.005;
            bioSphere.rotation.x += 0.003;
            bioSphere.rotation.y += targetX * 0.5;
            bioSphere.rotation.x += targetY * 0.5;
        }

        if (dnaGroup) {
            dnaGroup.rotation.y -= 0.008;
            dnaGroup.rotation.x = Math.sin(Date.now() * 0.001) * 0.15 + (targetY * 0.3);
        }

        if (particleCloud) {
            particleCloud.rotation.y += 0.001;
        }

        renderer.render(scene, camera);
    }

    // Launch when DOM is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();

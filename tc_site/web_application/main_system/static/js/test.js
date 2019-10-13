createLandscape({
  palleteImage:'img/pallete6.png',
})

function createLandscape(params){
  let container = document.querySelector("#oilcanvas")
  let width = container.width / 2.0
  let height = container.width / 2.0

  const fftSize = 128
  const mouse = { x:0, y:0, xDamped:0, yDamped:0 }
  /*
  const SPHERES = [{
      position: { type: "v2", value: new THREE.Vector2(0.5, 0.5) },
      radius: { type: "f", value: 0.2 }
    },
    {
      position: { type: "v2", value: new THREE.Vector2(0.3, 0.3) },
      radius: { type: "f", value: 0.3 }
    },
    {
      position: { type: "v2", value: new THREE.Vector2(0.9, 0.7) },
      radius: { type: "f", value: 0.4 }
    }
  ]
  */
 const SpheresLayers = [{ 
   value: [
    {position: new THREE.Vector2( 0.7, 0.5 ), radius: 0.35},
    {position: new THREE.Vector2( 0.4, 0.5 ), radius: 0.3},
    {position: new THREE.Vector2( 1.2, 0.7 ), radius: 0.1},
    {position: new THREE.Vector2( 0.8, 0.7 ), radius: 0.07},
    {position: new THREE.Vector2( 0.6, 0.9 ), radius: 0.14},
  ], 
  properties: {
      position: {},
      radius: {},
    } 
  },
  {
  value: [
    {position: new THREE.Vector2( 1.1, 1.2 ), radius: 0.1},
    {position: new THREE.Vector2( 0.4, 0.5 ), radius: 0.1},
    {position: new THREE.Vector2( 0.6, 0.7 ), radius: 0.06},
    {position: new THREE.Vector2( 0.8, 0.7 ), radius: 0.02},
    {position: new THREE.Vector2( 0.6, 0.4 ), radius: 0.06},
    {position: new THREE.Vector2( 0.4, 0.9 ), radius: 0.06},
    {position: new THREE.Vector2( 1.2, 0.3 ), radius: 0.06},
    {position: new THREE.Vector2( 0.6, 1.2), radius: 0.06},
  ], 
  properties: {
      position: {},
      radius: {},
    } 
  },
  {   
    value: [
    {position: new THREE.Vector2( 0.7, 1.2 ), radius: 0.25},
    {position: new THREE.Vector2( 0.5, 0.5 ), radius: 0.21},
    {position: new THREE.Vector2( 1.1, 0.2 ), radius: 0.06},
    {position: new THREE.Vector2( 1.2, 0.3 ), radius: 0.07},
    {position: new THREE.Vector2( 0.5, 0.4 ), radius: 0.18},
  ], 
  properties: {
      position: {},
      radius: {},
    } 
  },
  {
  value: [
    {position: new THREE.Vector2( 0.7, 0.5 ), radius: 0.1},
    {position: new THREE.Vector2( 0.4, 0.5 ), radius: 0.2},
    {position: new THREE.Vector2( 0.6, 0.7 ), radius: 0.1},
    {position: new THREE.Vector2( 0.8, 0.7 ), radius: 0.07},
    {position: new THREE.Vector2( 1.3, 0.9 ), radius: 0.14},
  ], 
  properties: {
      position: {},
      radius: {},
    } 
  },
];

  const colorPairs = 
  [
    {beginColor: new THREE.Vector3(0.6, 0.4, 0.6), endColor: new THREE.Vector3(1.0, 0.3, 0.5), alpha: 1.0, k: 0.32},
    {beginColor: new THREE.Vector3(0.8, 0.15, 0.4), endColor: new THREE.Vector3(1.0, 0.2, 0.3), alpha: 0.5, k: 0.86},
    {beginColor: new THREE.Vector3(1.0, 0.45, 0.5), endColor: new THREE.Vector3(0.8, 0.3, 0.6), alpha: 0.6, k: 0.35},
    {beginColor: new THREE.Vector3(0.9, 0.25, 0.4), endColor: new THREE.Vector3(1.0, 0.23, 0.7), alpha: 0.3, k: 0.36},
  ]

  const SpheresInitialPositionsValues = []
  for (let i = 0; i < SpheresLayers.length; ++i)
  {
    SpheresInitialPositionsValues.push(SpheresLayers[i].value.slice())
  }
  // const SphereAxis = SpheresLayerFirst.value.slice()

  let scene, renderer, camera
  let planeMeshes = []
  let elapsedSeconds

  let startTime = Date.now();
  init();

  function init(){
    sceneSetup()
    render()
    window.addEventListener("mousemove", onInputMove)
    window.addEventListener("resize", resize)
    resize()
    
    animateTitles()
  }

  function sceneSetup(){
    scene = new THREE.Scene()
    let fogColor = new THREE.Color( 0xffffff )

    planes()

    camera = new THREE.OrthographicCamera(width / -2,  width / 2,  height / -2, height / 2, 0.1, 1000)
    ambientLight = new THREE.AmbientLight(0xffffff, 1)
    scene.add(ambientLight)
    
    renderer = new THREE.WebGLRenderer( {
      canvas:container,
      antialias: true,
      alpha: true,
    } )
    
    camera.position.z = 0
    renderer.setPixelRatio = devicePixelRatio
    renderer.setSize(width, height)

  }

  function sceneTextures(){
    new THREE.TextureLoader().load( params.palleteImage, function(texture){
      terrainMesh.material.uniforms.pallete.value = texture
      terrainMesh.material.needsUpdate = true
    })
  }

  function planes()
  {
    for (let i = 0; i < SpheresLayers.length; ++i)
    {
      let planeFirst = new THREE.PlaneBufferGeometry(width, height, 1, 1);

      let invI = i;
      let uniforms = {
        time: { type: "f", value: 0.5 },
        ratioXtoY: { type: "f", value: width / height },
        colorBegin: { type: "v3", value: colorPairs[invI].beginColor},
        colorEnd: { type: "v3", value: colorPairs[invI].endColor},
        alpha: { type: "f", value: colorPairs[invI].alpha},
        kConst: { type: "f", value: colorPairs[invI].k},
        spheres: SpheresLayers[invI],
      }
      
      let material = new THREE.ShaderMaterial({
        uniforms: THREE.UniformsUtils.merge([ THREE.ShaderLib.basic.uniforms, uniforms ]),
        vertexShader: document.getElementById( 'jetbrains-vertex' ).textContent,
        fragmentShader: document.getElementById( 'jetbrains-fragment' ).textContent,
        side: THREE.DoubleSide,
        wireframe: false,
        transparent: true,
      })

      let firstPlaneMesh = new THREE.Mesh(planeFirst, material)
      firstPlaneMesh.position.z = -i - 1
      firstPlaneMesh.position.y = 0

      planeMeshes.push(firstPlaneMesh)
      scene.add(firstPlaneMesh)
    }
  }

  function resize(){
    width = window.innerWidth
    height = window.innerHeight / 2.0
    camera.aspect = width / height
    camera.updateProjectionMatrix()
    for (i = 0; i < planeMeshes.length; ++i)
    {
      planeMeshes[i].material.uniforms.ratioXtoY.value = camera.aspect
    }
    renderer.setSize( width, height )
  }

  function onInputMove(e){
    e.preventDefault()
    
    let x, y
    x = e.clientX
    y = e.clientY
    
    mouse.x = x
    mouse.y = y
  }

  function render(){
    requestAnimationFrame(render)

    mouse.xDamped = lerp(mouse.xDamped, mouse.x, 0.1)
    mouse.yDamped = lerp(mouse.yDamped, mouse.y, 0.1)

    let elapsedMilliseconds = Date.now() - startTime
    elapsedSeconds = elapsedMilliseconds * 0.001

    recalculateSpheresPositions()
    for (i = 0; i < planeMeshes.length; ++i)
    {
      let uniforms = planeMeshes[0].material.uniforms
      uniforms.alpha.value = colorPairs[i].alpha
      uniforms.kConst.value = colorPairs[i].k
      uniforms.time.value = elapsedSeconds
      uniforms.ratioXtoY.value = width / height
      uniforms.spheres.value = SpheresLayers[0].value
    }
    renderer.render(scene, camera)
  }

  function recalculateSpheresPositions()
  {
    for (i = 0; i < SpheresLayers.length; ++i)
    {
      let sphereLayer = SpheresLayers[i]
      let sphereInitialPosition = SpheresInitialPositionsValues[i]
      for (j = 0; j < sphereLayer.value.length; ++j) { 
        let radius = sphereLayer.value[j].radius
        let resultPoint = sphereLayer.value[j].position
        let initialPosition = sphereInitialPosition[j].position
        initialPosition.x += Math.sin(elapsedSeconds) / 250.0 * radius
        resultPoint.x += Math.sin(elapsedSeconds) / 250.0 * radius

        let dist = distance(resultPoint.x, resultPoint.y, mouse.xDamped / height, mouse.yDamped / height)
        let velocity = getVelocity(dist)
        let dx = resultPoint.x - mouse.xDamped / height
        let dy = resultPoint.y - mouse.yDamped / height
  
        let counterDist = distance(initialPosition.x, initialPosition.y, resultPoint.x, resultPoint.y)
        // let counterVelocity = getCounterVelocity(counterDist)
        resultPoint.x += (velocity * dx/dist)
        resultPoint.y += (velocity * dy/dist)
  
        let halfRadius = 0.5 * radius
        resultPoint.x = initialPosition.x + clamp(resultPoint.x - initialPosition.x, -halfRadius, halfRadius)
        resultPoint.y = initialPosition.y + clamp(resultPoint.y - initialPosition.y, -halfRadius, halfRadius)
      }
    }
  }

  function distance(x1, y1, x2, y2)
  {
    return Math.sqrt(Math.pow(y2 - y1, 2) + Math.pow(x2 - x1, 2))
  }

  function getVelocity(distance)
  {
    return (1 - smootherstep(0.0, 0.15, distance)) * 0.015;
  }

  function getCounterVelocity(distance)
  {
    return smootherstep(0.0, 0.15, distance) * 0.015;
  }

  function map (value, start1, stop1, start2, stop2) 
  {
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
  }

  function lerp (start, end, amt)
  {
    return (1 - amt) * start + amt * end
  }

  function clamp (val, start, end) 
  {
    return Math.max(start, Math.min(end, val))
  }

  function animateTitles() 
  {
    const overlay = document.querySelector('.overlay')
    TweenMax.to(overlay, 2, {
      ease: Quad.easeOut,
      opacity: 0
    });
  }

  function smootherstep(edge0, edge1, x) {
    // Scale, and clamp x to 0..1 range
    x = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
    // Evaluate polynomial
    return x * x * x * (x * (x * 6 - 15) + 10);
  }
}
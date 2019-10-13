createLandscape({
  palleteImage:'img/pallete6.png',
  coolRetroMusic: 'sound/music.ogg',
})

function createLandscape(params){
  let useMusic = true
  let useNativeMusic = false
  let musicPrevFrequency = 0.0

  let container = document.querySelector(".landscape")
  let width = window.innerWidth
  let height = window.innerHeight

  const fftSize = 128
  const mouse = { x:0, y:0, xDamped:0, yDamped:0 }

  let scene, renderer, camera
  let terrainMesh, redSunMesh, neonGridMesh, analyser

  let startTime = Date.now();
  document.body.addEventListener('click', init, true)
  // init();

  function init(){
    sceneSetup()
    createAudio()
    sceneElements()
    sceneTextures()
    render()
    window.addEventListener("mousemove", onInputMove)
    window.addEventListener("resize", resize)
    resize()
    
    animateTitles()
    document.body.removeEventListener("click", init, true)
  }

  function sceneSetup(){
    scene = new THREE.Scene()
    let fogColor = new THREE.Color( 0xffffff )
    scene.background = fogColor
    scene.fog = new THREE.Fog(fogColor, 30, 400)

    sky()
    redSun()
    setupNeonGridMesh()

    camera = new THREE.PerspectiveCamera(60, width / height, 0.01, 10000)
    camera.position.y = 8
    camera.position.z = 10
    
    ambientLight = new THREE.AmbientLight(0xffffff, 1)
    scene.add(ambientLight)
    
    renderer = new THREE.WebGLRenderer( {
      canvas:container,
      antialias: true,
      alpha: true,
    } )
    
    renderer.setPixelRatio = devicePixelRatio
    renderer.setSize(width, height)

  }

  function createAudio(){
    let listener = new THREE.AudioListener()

		let audio = new THREE.Audio( listener )

		let mediaElement = new Audio( 'sound/music.ogg' )
		mediaElement.loop = true
		mediaElement.play()

		audio.setMediaElementSource( mediaElement )

		analyser = new THREE.AudioAnalyser( audio, fftSize )
  }

  function sceneElements(){

    let geometry = new THREE.PlaneBufferGeometry(100, 400, 20, 20)

    let uniforms = {
      time: { type: "f", value: 0.0 },
      distortCenter: { type: "f", value: 0.1 },
      roadWidth: { type: "f", value: 1.5 },
      pallete:{ type: "t", value: null},
      speed: { type: "f", value: 0.5 },
      maxHeight: { type: "f", value: 10.0 },
      color: new THREE.Color(1, 1, 1),
      cpuAudioData: { type: "f", value: 0.0 },
      audioData: { value: new THREE.DataTexture( analyser.data, fftSize / 2, 1, THREE.LuminanceFormat ) },
    }

    let defines = {
      USE_GRID: false,
      USE_MUSIC: useMusic,
      USE_MUSIC_NATIVE: useNativeMusic,
    }
    
    let material = new THREE.ShaderMaterial(
      {
        uniforms: THREE.UniformsUtils.merge([ THREE.ShaderLib.basic.uniforms, uniforms ]),
        vertexShader: document.getElementById( 'custom-vertex' ).textContent,
        fragmentShader: document.getElementById( 'custom-fragment' ).textContent,
        side: THREE.BothSide,
        wireframe:false,
        fog:true,
        defines: defines,
      }
    )

    terrainMesh = new THREE.Mesh(geometry, material)
    terrainMesh.position.z = -180
    terrainMesh.rotation.x = -Math.PI / 2

    scene.add(terrainMesh)

  }

  function sceneTextures(){
    new THREE.TextureLoader().load( params.palleteImage, function(texture){
      terrainMesh.material.uniforms.pallete.value = texture
      terrainMesh.material.needsUpdate = true
    })
  }

  function sky(){
    sky = new THREE.Sky();
    sky.scale.setScalar( 450000 );
    sky.material.uniforms.turbidity.value = 1;
    sky.material.uniforms.rayleigh.value = 0.01;
    sky.material.uniforms.luminance.value = 1;
    sky.material.uniforms.mieCoefficient.value = 0.0003;
    sky.material.uniforms.mieDirectionalG.value = 0.99995;
    
    scene.add( sky );

    sunSphere = new THREE.Mesh(
      new THREE.SphereBufferGeometry( 0, 0, 0),
      new THREE.MeshBasicMaterial( { color: 0xffffff } )
    );
    sunSphere.visible = false;
    scene.add( sunSphere );
    
    let theta = Math.PI * ( -0.03 )
    let phi = 2 * Math.PI * ( -.25 )

    sunSphere.position.x = 400000 * Math.cos( phi )
    sunSphere.position.y = 2000000 * Math.sin( phi ) * Math.sin( theta )
    sunSphere.position.z = 400000 * Math.sin( phi ) * Math.cos( theta )
    
    sky.material.uniforms.sunPosition.value.copy( sunSphere.position )

    let starsGeometry = new THREE.Geometry()

    for ( let i = 0; i < 600; i ++ ) {

      let star = new THREE.Vector3()
      star.x = THREE.Math.randFloatSpread( 1000 )
      star.y = THREE.Math.randFloatSpread( 1000 )
      star.z = THREE.Math.randFloat( -700, -501)

      starsGeometry.vertices.push( star )

    }

    let starsMaterial = new THREE.PointsMaterial( { color: 0xffffff, size: 2.0 } )

    let starField = new THREE.Points( starsGeometry, starsMaterial )

    scene.add( starField )
  }

  function redSun()
  {
    let redSun = new THREE.PlaneBufferGeometry(320, 320, 1, 1);

    let uniforms = {
      time: { type: "f", value: 0.5 }
    }

    let material = new THREE.ShaderMaterial({
      uniforms: THREE.UniformsUtils.merge([ THREE.ShaderLib.basic.uniforms, uniforms ]),
      vertexShader: document.getElementById( 'sun-vertex' ).textContent,
      fragmentShader: document.getElementById( 'sun-fragment' ).textContent,
      side: THREE.FrontSide,
      wireframe: false,
      transparent: true,
    })

    redSunMesh = new THREE.Mesh(redSun, material)
    redSunMesh.position.z = -500
    redSunMesh.position.y = 50

    scene.add(redSunMesh)
  }

  function setupNeonGridMesh()
  {
    let neonGrid = new THREE.PlaneBufferGeometry(100, 400, 1, 1)

    let uniforms = {
      time: { type: "f", value: 0.5 }
    }

    let material = new THREE.ShaderMaterial({
      uniforms: THREE.UniformsUtils.merge([ THREE.ShaderLib.basic.uniforms, uniforms ]),
      vertexShader: document.getElementById( 'sun-vertex' ).textContent,
      fragmentShader: document.getElementById( 'grid-fragment' ).textContent,
      side: THREE.BothSide,
      wireframe: false,
      transparent: true,
    })

    neonGridMesh = new THREE.Mesh(neonGrid, material)
    neonGridMesh.position.z = -180
    neonGridMesh.position.y += 1
    neonGridMesh.rotation.x = -Math.PI / 2

    scene.add(neonGridMesh)
  }

  function resize(){
    width = window.innerWidth
    height = window.innerHeight
    camera.aspect = width / height
    camera.updateProjectionMatrix()
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

    analyser.getFrequencyData()
    if (useNativeMusic)
    {
      terrainMesh.material.uniforms.audioData.value.needsUpdate = true
    }
    else if (useMusic)
    {
      var currentFrecuency = frequencyClampedFormula(analyser.getAverageFrequency())
      musicPrevFrequency = lerp(musicPrevFrequency, currentFrecuency, 0.1)
      terrainMesh.material.uniforms.cpuAudioData.value = musicPrevFrequency
    }

    mouse.xDamped = lerp(mouse.xDamped, mouse.x, 0.1)
    mouse.yDamped = lerp(mouse.yDamped, mouse.y, 0.1)

    let elapsedMilliseconds = Date.now() - startTime
    let elapsedSeconds = elapsedMilliseconds * 0.001
    terrainMesh.material.uniforms.time.value = elapsedSeconds
    terrainMesh.material.uniforms.distortCenter.value = map(mouse.xDamped, 0, width, -0.1, 0.1)
    terrainMesh.material.uniforms.maxHeight.value = map(mouse.yDamped, 0, height, 20, 10)

    redSunMesh.material.uniforms.time.value = elapsedSeconds
    let centeredDump = map(mouse.xDamped, 0, width, - width / 2, width / 2)
    redSunMesh.position.x = -(centeredDump / 30.0)
    neonGridMesh.material.uniforms.time.value = elapsedSeconds

    renderer.render(scene, camera)

  }

  function frequencyClampedFormula(normalFrequency)
  {
    let normalizedFrequency = clamp(normalFrequency / 100.0 - 1.0, 0, 1.0)
    return squared(normalizedFrequency * 4.0);
  }

  function squared(x)
  {
    return x * x * x
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
}
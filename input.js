//This file will contain the input mapping

//values
const ONE = 1;


//keys
const W = 'KeyW'
const S = 'KeyS'
const A = 'KeyA'
const D = 'KeyD'
const E = 'KeyE'
const Q = 'KeyQ'

//CAMERA CONTROLS

//camera pan controls
window.addEventListener('keydown', function(event){

    
    if(event.code == W){
        camera.position.z -= ONE; //pans camera up

    }
    if(event.code == S){
        camera.position.z += ONE; //pans camera down

    }
    if(event.code == A){
        camera.position.x -= ONE; //pans camera left

    }
    if(event.code == D){
        camera.position.x += ONE; //pans camera right

    }
    if(event.code == E){
        camera.position.y += ONE; //pans camera up

    }
    if(event.code == Q){
        camera.position.y -= ONE; //pans camera up

    }

});
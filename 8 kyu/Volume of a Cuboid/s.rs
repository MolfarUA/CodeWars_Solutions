58261acb22be6e2ed800003a


fn get_volume_of_cuboid(length: f32, width: f32, height: f32) -> f32 {
    length * width * height
}
_____________________________
fn get_volume_of_cuboid(length: f32, width: f32, height: f32) -> f32 {
    
    struct cuboid {
        leng: f32,
        wid: f32,
        hei: f32,
    };
    
    let ex_cuboid = cuboid {
        leng: length,
        wid: width,
        hei: height,
    };
    
    ex_cuboid.leng * ex_cuboid.wid * ex_cuboid.hei
}
_____________________________
fn get_volume_of_cuboid(length: f32, width: f32, height: f32) -> f32 {
    length*width*height as f32
}



///////  D3 FILE FOR REDERING PET PHOTOS //////////


// d3.select("#selPets").on("click", function(){

//     var pets = changepets(d3.select('#selPets option:checked').text())



// })

function changepets(petoption){
    console.log("petoption",petoption)
    d3.select("#petpic").attr("src", petoption);

}


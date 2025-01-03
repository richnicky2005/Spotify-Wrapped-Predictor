async function FetchUserData(){
    try {
        const response = await fetch('/wrapped'); 
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        var data = await response.json()

        var profile = data.profile
        var topTracks = data.topTracks.items
        var topArtists = data.topArtists.items

        DisplayData(profile,topTracks)
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function DisplayData(profile){
    var profilePic = document.getElementsByClassName("profile-picture")[0]
    if(profile.images[0].url){
        profilePic.src = profile.images[0].url
    }
    else{
        profilePic.src = "www.google.com"
    }
    var profileUsername = document.getElementsByClassName("profile-info")[0]
    profileUsername.getElementsByTagName("h1")[0].innerHTML = 'Welcome, '+ profile.id

    



}

FetchUserData()

async function FetchUserData(){
    try {
        const response = await fetch('/wrapped'); // Replace with your server endpoint
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        var data = await response.json()

        var profile = data.profile
        var topTracks = data.topTracks.items
        var topArtists = data.topArtists.items

        DisplayData(profile)
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function DisplayData(profile){
    var profilePic = document.getElementsByClassName("profile-picture")
    profilePic.src = profile.images[0].url
    var profileUsername = document.getElementsByClassName("profile-info")
    profileUsername.getElementsByTagName("h1").innerHTML = 'Welcome, '+ profile.id
}

FetchUserData()

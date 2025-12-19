.msglist {
    align-items:flex;
    overflow-y: scroll;
    max-height: 92%;
    flex-direction: column;
    
    display: flex;
    align-items: flex-start;
    scrollbar-width: none;
    z-index: 1;
    position: relative;
    box-sizing: border-box;
    padding-right: 15px;
    top: 0;
    width: calc(100% - var(--sidebar-width) - calc(var(--finder-width) ));
    left: var(--sidebar-width);
    transition: 0.25s ease-in-out;
}
button {
    border-color: rgb(0,0,0,1);
    font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-size: 1rem;
  font-weight: 600;
  all:unset;
  background-color: #ffffff;
  user-select: none;
  transition: 0.05s linear;
}
button:hover {
    background-color: #dddd;
}

.channel-button {
    width: 100%;
    height: 60px;
    border-radius: 5px;
    background-color: var(--primary-color);
    font-size: 14px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    text-align: center;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}
:root {
    --sidebar-width: 150px;
    --primary-color: #bb86fc;
    --second-color: #754242;
    --finder-width: 400px;
    --darkened-color: color-mix(in srgb, var(--second-color) 80%, black);
}
.msglist::-webkit-scrollbar {
    display: none;             
}

.reply-text {
    font-size: 11px;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.reply-img {
    width: 16px;
    height:16px;
    border-radius: 25px;
}

.reply {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 6px;
}
.channels-name {
    border-bottom: 2px dashed black;
    font-size: 16px !important;
    text-align: left;
}
/* Add to base.css */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100vh;

    z-index: 100;
    padding: 20px 10px 10px 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    backdrop-filter: blur(3px);
    transition: transform 0.25s ease-in-out, width 0.25s ease-in-out, opacity 0.25s;
    transform: translateX(calc(-1 * (var(--sidebar-width) - 15px))); /* Collapsed offset */
    background-color: var(--darkened-color);
    
}
.sidebar h3 {
    margin-top: 0;
    font-size: 1.2em;
    text-align: center;
}


.lobby-searcher {
    position: fixed;
    z-index: 9999;
    top: 0;
    right: 0;
        width: var(--finder-width);
    height: 100vh;
    background: rgba(204, 204, 204, 0.5);
    display: flex;
    flex-direction: column;
    gap: 10px;
    backdrop-filter: blur(3px);
    transition: transform 0.25s ease-in-out, width 0.25s ease-in-out, opacity 0.25s;
    transform: translateX(400px);
    

}
#channelList {
    list-style: none;
    padding: 0;
    margin: 0;
    min-height: 74%;
    overflow-y: auto;
}

span {
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}


.bottom-part {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: column;
  position: fixed;
  bottom: 5%;
  width: 85%;
}

.profile-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile_photo {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-bottom: 4px;
}

.text {
    display: flex;
    flex-direction: column;
}

.username {
  text-align:center;
  font-size: 14px;
  
}

.version {
  text-align:center;
  font-size: 20px;

}
#channelList li {
    padding: 8px 12px;
    margin-bottom: 6px;
    border-radius: 4px;
    height: 50px;
    font-size: 20px;
    cursor: pointer;
    background-color: var(--primary-color);
    transition: background 0.15s;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.selected-channel {
    font-weight: bold;
    font-size: 20px;
}
#channelList li:hover {
    background: var(--second-color);
    font-weight: bold;
}
.headeritems {
    display: flex;
    align-items: center; /* Center items vertically */
    flex-direction: row;
    height: auto;
    position: relative;
    width: 75%;
    justify-content: space-between; /* This spreads items across the container */
    border-radius: 5px;
    transition: 0.25s ease-in-out;
    background:rgba(225, 225, 225, 0.5);
    backdrop-filter: blur(3px);
    z-index: 99999999999;
}

.lobbysettings {
    margin-left: 1%;
    width: 32px;
    height: 32px;
    transition: 0.125s;
    scale: 1;
}


.lobbysettings:active {
    scale: 1.2;
}

.header {
    display: flex;
    align-items: center;        /* Vertically center children */
    justify-content: center;    /* Horizontally center children */              /* Example height */
    transition: 0.25s;
    position: relative;
    transform: translateY(-100%);
    z-index: 999999999999;
}

.header.show {
    transform: translateY(0); /* Shows the bar */
  }
.rightHeader flex {
    flex-direction: column;
    align-items: center; /* Align children to the right */
    margin-left: auto; /* Push to the right */

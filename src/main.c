#include "../include/common.h"
static const unsigned short kong_unlocked_flags[] = {
	385,
	6,
	70,
	66,
	117,
};

enum map_values {
	NINTENDO_LOGO = 40,
	MAIN_MENU = 80,
	BANJOS_HOUSE = 29,
	SPIRAL_MOUNTAIN = 171,
	LAIR_ENTRANCE = 169,
	LAIR_F2 = 173,
	LAIR_F3 = 174,
	LAIR_TTC_ENTRANCE = 175,
	LAIR_PIPE_ROOM = 178,
	MUMBOS_MOUNTAIN = 19,
	TICKERS_TOWER = 21,
	MUMBOS_SKULL = 22,
	TREASURE_TROVE_COVE = 90,
	SANDCASTLE = 91,
	BLUBBERS_SHIP = 92,
	DIVE_BARREL = 177
};

enum level_type {
	LEVEL_TYPE_JAPES = 0x0,
	LEVEL_TYPE_AZTEC = 0x1,
	LEVEL_TYPE_FACTORY = 0x2,
	LEVEL_TYPE_ISLES = 0x7,
	LEVEL_TYPE_BONUS = 0x9
};

enum song_values {
	S_SPIRAL_MOUNTAIN = 49,
	S_LAIR = 105,
	S_MENU = 106,
	S_TICKERS_TOWER = 28,
	S_MUMBOS_HUT = 53,
	S_MUMBOS_MOUNTAIN = 56,
	S_TREASURE_TROVE_COVE = 68,
	S_INSIDE_SANDCASTLE = 70,
	S_FURNACE_FUN = 77
	//valid = 74,77,78,79,80
};

enum skybox_values {
	SKY_LIGHT = 46,
	SKY_GREEN = 47,
	SKY_SUNSET = 48,
	SKY_BLACK = 49
};

enum collectable_kong {
	ANY = 0,
	DK = 2,
	DIDDY = 3,
	LANKY = 4,
	TINY = 5,
	CHUNKY = 6
};

typedef struct angle_struct {
	int map;
	int exit;
	short angle;
} angle_struct;

angle_struct map_angles[] = {
	[0].map = SPIRAL_MOUNTAIN,
	[0].exit = 0,
	[0].angle = 0x0805,
	
	[1].map = SPIRAL_MOUNTAIN,
	[1].exit = 1,
	[1].angle = 0x0000,
	
	[2].map = LAIR_ENTRANCE,
	[2].exit = 0,
	[2].angle = 0x0805,
	
	[3].map = LAIR_ENTRANCE,
	[3].exit = 1,
	[3].angle = 0x019F,
	
	[4].map = LAIR_ENTRANCE,
	[4].exit = 2,
	[4].angle = 0x0D9C,
	
	[5].map = LAIR_F2,
	[5].exit = 0,
	[5].angle = 0x0A5F,
	
	[6].map = LAIR_F2,
	[6].exit = 1,
	[6].angle = 0x0FE9,
	
	[7].map = LAIR_F3,
	[7].exit = 0,
	[7].angle = 0x0C9A,
	
	[8].map = LAIR_F3,
	[8].exit = 1,
	[8].angle = 0x071F,
	
	[9].map = LAIR_F3,
	[9].exit = 2,
	[9].angle = 0x0002,
	
	[10].map = LAIR_TTC_ENTRANCE,
	[10].exit = 0,
	[10].angle = 0x0000,
	
	[11].map = LAIR_TTC_ENTRANCE,
	[11].exit = 1,
	[11].angle = 0x061C,
	
	[12].map = LAIR_PIPE_ROOM,
	[12].exit = 0,
	[12].angle = 0x00,
	
	[13].map = MUMBOS_MOUNTAIN,
	[13].exit = 0,
	[13].angle = 0x0A95,
	
	[14].map = MUMBOS_MOUNTAIN,
	[14].exit = 1,
	[14].angle = 0x03A1,
	
	[15].map = MUMBOS_MOUNTAIN,
	[15].exit = 2,
	[15].angle = 0x01A7,
	
	[16].map = MUMBOS_MOUNTAIN,
	[16].exit = 3,
	[16].angle = 0x0E6B,
	
	[17].map = TICKERS_TOWER,
	[17].exit = 0,
	[17].angle = 0x0F90,
	
	[18].map = MUMBOS_SKULL,
	[18].exit = 0,
	[18].angle = 0x0800,
	
	[19].map = TREASURE_TROVE_COVE,
	[19].exit = 0,
	[19].angle = 0x0800,
	
	[20].map = TREASURE_TROVE_COVE,
	[20].exit = 1,
	[20].angle = 0x0000,
	
	[21].map = TREASURE_TROVE_COVE,
	[21].exit = 2,
	[21].angle = 0x0000,
	
	[22].map = TREASURE_TROVE_COVE,
	[22].exit = 3,
	[22].angle = 0x0800,
	
	[23].map = TREASURE_TROVE_COVE,
	[23].exit = 4,
	[23].angle = 0x0000,
	
	[24].map = SANDCASTLE,
	[24].exit = 0,
	[24].angle = 0x0800,
	
	[25].map = BLUBBERS_SHIP,
	[25].exit = 0,
	[25].angle = 0x0800,
	
	[26].map = BANJOS_HOUSE,
	[26].exit = 0,
	[26].angle = 0x0800
};

enum note_door_values {
	NOTE_DOOR_1 = 75
};

void setInitialMap(char,char);
void startupSkip();
void unlockKongs();
void unlockMoves();

void updateSongList();
void updateLevelTypes();
void updateCollectableFlagTable();
void initMapAngles();
void setFacingAngle(int, int);
void setDefaultSkybox(short);
void moveLoadingZone(int, short, short, short);
void giveInfinites();
void setMenuInitialPosition(float,float,float);
void setLobbyWarps();

int* displayListModifiers(int*);
int* displayCredits(int*);
int* displayMenuText(int*);
int* displayCoin(int*);
int* displaySpiralText(int*);
int* displayNoteDoorText(int*);
int* displayBunch(int*);
int* displayWarpText(int*);
char checkRadialDistance(float, float, float);
int getJiggyCount();
int getCBCount();
int getDKCoinCount();

void cFuncLoop(void) {
	// Enable stack trace upon crash
	*(s8 *)(0x807563B4) = 1;
	*(s32 *)(0x80731F78) = 0;
	/*
		This function is run every frame. Place c code which you are wanting to be run every frame
	*/
	setInitialMap(SPIRAL_MOUNTAIN,0);
	startupSkip();
	StorySkip = 1;
	
	//tag anywhere
	initHack();
	tagAnywhere();
	
	//skybox hack to pre-load next skybox texture
	//also set initial facing angle
	if(LZFadeoutProgress >= 25.0f) {
		CurrentMap = DestMap;
		if(LZFadeoutProgress > 0.0f) {
			setFacingAngle(DestMap, DestExit);
		}
	}
	
	switch(CurrentMap) {
		case NINTENDO_LOGO:
			updateSongList();
			updateLevelTypes();
			updateCollectableFlagTable();
			break;
		case LAIR_ENTRANCE:
			setPermanentFlag(382); //B Locker FTT
			if(!checkFlag(461,0)) { //if MM B Locker not cleared
				moveLoadingZone(MUMBOS_MOUNTAIN, 0, 2000, 0);//move LZ
			} else {
				moveLoadingZone(MUMBOS_MOUNTAIN, 1182, 4, 397);
			}
			if(getCBCount() < NOTE_DOOR_1) { //NOTE DOOR REQUIREMENT == 75
				moveLoadingZone(LAIR_F2, 0, 2000, 0);
			} else {
				moveLoadingZone(LAIR_F2, 33, 218, 36);
			}
			break;
		case LAIR_F2:
			break;
		case LAIR_F3:
			if(checkRadialDistance(2500.0f,90.8f, 119.9f)) {
				if(NewlyPressedControllerInput.Buttons.l) {
					moveLoadingZone(BANJOS_HOUSE, (short)Player->xPos,(short)Player->yPos,(short)Player->zPos);
					playSound(SFX_TakeWarp, 0x4FFF, 63.0f, 1.0f, 0, 0);
				}
			}
			break;
		case LAIR_TTC_ENTRANCE:
			if(!checkFlag(462,0)) { //if TTC B Locker not cleared
				moveLoadingZone(TREASURE_TROVE_COVE, 0, 2000, 0);//move LZ
			} else {
				moveLoadingZone(TREASURE_TROVE_COVE, 201,30,471);
			}
			break;
		case LAIR_PIPE_ROOM:
			break;
		case SPIRAL_MOUNTAIN:
			if(getDKCoinCount() < 5) {
				moveLoadingZone(LAIR_ENTRANCE, 0, 2000, 0);
			} else {
				moveLoadingZone(LAIR_ENTRANCE, 1166, 314, 656);
			}
			setDefaultSkybox(SKY_LIGHT);
			break;
		case MUMBOS_MOUNTAIN:
			if(DestMap == 7) { //fix deathwarp to japes
				DestMap = MUMBOS_MOUNTAIN;
			}
			setLobbyWarps();
			setDefaultSkybox(SKY_GREEN);
			break;
		case TICKERS_TOWER:
			if(DestMap == 7) { //fix deathwarp to japes
				DestMap = MUMBOS_MOUNTAIN;
			}
			setLobbyWarps();
			Player->slipping_speed = 0.0f;
			break;
		case MUMBOS_SKULL:
			if(DestMap == 7) { //fix deathwarp to japes
				DestMap = MUMBOS_MOUNTAIN;
			}
			setLobbyWarps();
			setPermanentFlag(383); //tbarrels spawned
			break;
		case TREASURE_TROVE_COVE:
			setLobbyWarps();
			setDefaultSkybox(SKY_SUNSET);
			giveInfinites();
			break;
		case SANDCASTLE:
			setLobbyWarps();
			break;
		case BLUBBERS_SHIP:
			setLobbyWarps();
			break;
		case MAIN_MENU:
			setDefaultSkybox(SKY_LIGHT);
			menuCutsceneIndex = 0x02;
			menuIntroCS = 0x0A;
			setMenuInitialPosition(1712.0f,0.5f,1891.7f);
			break;
		case BANJOS_HOUSE:
			setDefaultSkybox(SKY_LIGHT);
			break;
		default:
			setDefaultSkybox(SKY_BLACK);
			break;
	}
	
	//fix lair music and skybox
	switch(CurrentMap) {
		case LAIR_ENTRANCE:
		case LAIR_F2:
		case LAIR_F3:
		case LAIR_PIPE_ROOM:
		case LAIR_TTC_ENTRANCE:
			setDefaultSkybox(SKY_BLACK);
			if(*(s32 *)(0x8076BF54) >= 0x16600) {
				*(s16 *)(0x807458DC) = 92;
			} else {
				*(s16 *)(0x807458DC) = S_LAIR;
			}
			break;
	}
	
	unlockKongs();
	unlockMoves();
}

//modifies warpOutOfLevel
void setLobbyWarps() {
	short map = 0x00;
	short exit = 0x00;
	switch(CurrentMap) {
		case MUMBOS_MOUNTAIN:
		case TICKERS_TOWER:
		case MUMBOS_SKULL:
			map = LAIR_ENTRANCE;
			exit = 2;
			break;
		case TREASURE_TROVE_COVE:
		case SANDCASTLE:
		case BLUBBERS_SHIP:
			map = LAIR_TTC_ENTRANCE;
			exit = 1;
			break;
	}
	
	//NOP
	*(int*)(0x80600064) = 0;
	
	//LUI A0, MAP
	*(short*)(0x8060006C) = 0x2404; //LI A0
	*(short*)(0x8060006E) = map;	//MAP
	
	//LI A1, EXIT
	*(short*)(0x8060005C) = 0x2405; //LI A1
	*(short*)(0x8060005E) = exit;	//EXIT
}

void setMenuInitialPosition(float xpos, float ypos, float zpos) {
	if(Player) {
		Player->xPos = xpos;
		Player->zPos = zpos;
		menuDKyPos = -ypos;
	}
}

void setInitialMap(char map, char exit) {
	*(char *)(0x80714547) = map;
	*(char *)(0x8071455B) = exit;
}

void startupSkip() {
	*(char *)(0x807132BF) = 0x50;
	*(char *)(0x807132CB) = 0x5;
}

void unlockKongs() {
	for(int i=0; i<5; ++i) {
		setFlag(kong_unlocked_flags[i],1,0);
	}
}

void unlockMoves() {
	for(int kong_number=0; kong_number<5; ++kong_number) {
		*(s8 *)(0x807FC950 + kong_number*0x5E + 0) = 3;
	}
}

void giveInfinites() {
	*(s16 *)(0x807FCC40 + 0) = 99; //ammo
	*(s16 *)(0x807FCC40 + 6) = 99; //crystals
}

void setDefaultSkybox(short sky) {
	*(int *)(0x807079F0) = 0x00000000;
	*(short*)(0x80707A72) = sky;
}

void updateCollectableFlagTable() {
	CollectableFlagTable[0].map = MUMBOS_MOUNTAIN;
	CollectableFlagTable[0].model2_id = 0x1F;
	CollectableFlagTable[0].collectable_state = ANY;
	
	CollectableFlagTable[1].map = MUMBOS_MOUNTAIN;
	CollectableFlagTable[1].model2_id = 0x2D;
	CollectableFlagTable[1].collectable_state = ANY;
	
	CollectableFlagTable[2].map = MUMBOS_MOUNTAIN;
	CollectableFlagTable[2].model2_id = 0x3B;
	CollectableFlagTable[2].collectable_state = ANY;
	
	CollectableFlagTable[3].map = MUMBOS_MOUNTAIN;
	CollectableFlagTable[3].model2_id = 0x47;
	CollectableFlagTable[3].collectable_state = ANY;
	
	CollectableFlagTable[4].map = MUMBOS_MOUNTAIN;
	CollectableFlagTable[4].model2_id = 0x4B;
	CollectableFlagTable[4].collectable_state = ANY;
	
	CollectableFlagTable[5].map = LAIR_ENTRANCE;
	CollectableFlagTable[5].model2_id = 0x00;
	CollectableFlagTable[5].collectable_state = ANY;
	
	CollectableFlagTable[6].map = LAIR_F2;
	CollectableFlagTable[6].model2_id = 0x00;
	CollectableFlagTable[6].collectable_state = ANY;
	
	CollectableFlagTable[7].map = LAIR_F3;
	CollectableFlagTable[7].model2_id = 0x01;
	CollectableFlagTable[7].collectable_state = ANY;
	
	CollectableFlagTable[8].map = LAIR_PIPE_ROOM;
	CollectableFlagTable[8].model2_id = 0x00;
	CollectableFlagTable[8].collectable_state = ANY;
	
	CollectableFlagTable[9].map = LAIR_TTC_ENTRANCE;
	CollectableFlagTable[9].model2_id = 0x00;
	CollectableFlagTable[9].collectable_state = ANY;
	
	CollectableFlagTable[10].map = TREASURE_TROVE_COVE;
	CollectableFlagTable[10].model2_id = 0x17;
	CollectableFlagTable[10].collectable_state = ANY;
	
	CollectableFlagTable[11].map = TREASURE_TROVE_COVE;
	CollectableFlagTable[11].model2_id = 0x2D;
	CollectableFlagTable[11].collectable_state = ANY;
	
	CollectableFlagTable[12].map = TREASURE_TROVE_COVE;
	CollectableFlagTable[12].model2_id = 0x4D;
	CollectableFlagTable[12].collectable_state = ANY;
	
	CollectableFlagTable[13].map = SANDCASTLE;
	CollectableFlagTable[13].model2_id = 0x00;
	CollectableFlagTable[13].collectable_state = ANY;
	
	CollectableFlagTable[14].map = BLUBBERS_SHIP;
	CollectableFlagTable[14].model2_id = 0x00;	
	CollectableFlagTable[14].collectable_state = ANY;
}

//Updates pause menu options
void updateLevelTypes() {
	for(int map=0; map<0xDC; ++map) {
		switch(map) {
			//Overworld
			case BANJOS_HOUSE:
			case SPIRAL_MOUNTAIN:
			case LAIR_F3:
			case LAIR_TTC_ENTRANCE:
			case LAIR_PIPE_ROOM:
				LevelIndexes[map] = LEVEL_TYPE_ISLES;
				break;
			
			//Levels AND Lobbies
			case LAIR_ENTRANCE: //lobby
			case MUMBOS_MOUNTAIN:
			case TICKERS_TOWER:
			case MUMBOS_SKULL:
				LevelIndexes[map] = LEVEL_TYPE_JAPES;
				break;
			case LAIR_F2: //lobby
			case TREASURE_TROVE_COVE:
			case SANDCASTLE:
			case BLUBBERS_SHIP:
				LevelIndexes[map] = LEVEL_TYPE_AZTEC;
				break;
		}
	}
}

void moveLoadingZone(int map, short x, short y, short z) {
	if(loadingZoneArray) {
		for(int i=0; i<loadingZoneArraySize; ++i) {
			LoadingZone *temp = &loadingZoneArray[i];
			if(temp->dest_map == map) {
				temp->xpos = x;
				temp->ypos = y;
				temp->zpos = z;
			}
		}
	}
}

void setFacingAngle(int current_map, int current_exit) {
	for(int i=0; i<27; ++i) {
		if(	map_angles[i].map == current_map && map_angles[i].exit == current_exit) {
			if(Player) {
				Player->facing_angle = map_angles[i].angle;
			}
			break;
		}
	}
}

void updateSongList() {
	for(int i=0; i<0xC0; ++i) {
		switch(i) {
			case MAIN_MENU:
			case BANJOS_HOUSE:
			case SPIRAL_MOUNTAIN:
			case LAIR_ENTRANCE:
			case LAIR_F2:
			case LAIR_F3:
			case LAIR_TTC_ENTRANCE:
			case LAIR_PIPE_ROOM:
			case MUMBOS_MOUNTAIN:
			case TICKERS_TOWER:
			case TREASURE_TROVE_COVE:
			case SANDCASTLE:
			case BLUBBERS_SHIP:
				songArray[i].song = 0x00;
				songArray[i].unk1 = 0x00;
				songArray[i].unk2 = 0x00;
				songArray[i].unk3 = 0x00;
			default:
				break;
		}
	}
	
	songArray[MAIN_MENU].song = S_MENU;
	songArray[BANJOS_HOUSE].song = S_FURNACE_FUN;
	songArray[SPIRAL_MOUNTAIN].song = S_SPIRAL_MOUNTAIN;
	songArray[LAIR_ENTRANCE].song = S_LAIR;
	songArray[LAIR_F2].song = S_LAIR;
	songArray[LAIR_F3].song = S_LAIR;
	songArray[LAIR_TTC_ENTRANCE].song = S_LAIR;
	songArray[LAIR_PIPE_ROOM].song = S_LAIR;
	songArray[MUMBOS_MOUNTAIN].song = S_MUMBOS_MOUNTAIN;
	songArray[TICKERS_TOWER].song = S_TICKERS_TOWER;
	songArray[MUMBOS_SKULL].song = S_MUMBOS_HUT;
	songArray[TREASURE_TROVE_COVE].song = S_TREASURE_TROVE_COVE;
	songArray[SANDCASTLE].song = S_INSIDE_SANDCASTLE;
	songArray[BLUBBERS_SHIP].song = S_TREASURE_TROVE_COVE;
}

//DisplayList stuff
int* displayListModifiers(int* dl) {
	float draw_distance;
	switch(CurrentMap) {
		case MAIN_MENU:
			dl = displayMenuText(dl);
			break;
		case BANJOS_HOUSE:
			dl = displayCredits(dl);
			break;
		case SPIRAL_MOUNTAIN:
			if(checkRadialDistance(2500.0f,1167.2f, 1068.9f) && getDKCoinCount() < 5) {
				dl = displaySpiralText(dl);
				dl = displayCoin(dl);
			}
			break;
		case LAIR_ENTRANCE:
			if(checkRadialDistance(3600.0f,63.6f, 70.6f) && getCBCount() < NOTE_DOOR_1) {
				dl = displayNoteDoorText(dl);
				dl = displayBunch(dl);
			}
			break;
		case LAIR_F3:
			if(checkRadialDistance(2000.0f,90.8f, 119.9f)) {
				dl = displayWarpText(dl);
			}
			break;
	}
	return dl;
}

char checkRadialDistance(float threshold_squared, float x, float z) {
	if(Player) {
		float xpos = Player->xPos;
		float zpos = Player->zPos;
		return ((xpos - x) * (xpos - x) + (zpos - z) * (zpos - z)) < threshold_squared;
	}
	return 0;
}

int* displayMenuText(int* dl) {
	dl = drawTextContainer(dl, 1, 25, 525, "BANJO KONGZOOIE", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 25, 550, "BY GLORIOUSLIAR", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	return dl;
}

int* displayCredits(int* dl) {
	int jiggies = getJiggyCount();
	int cbs = getCBCount();
	int coins = getDKCoinCount();
	char jiggy_text[42], cb_text[42], coin_text[25];
	dk_strFormat(jiggy_text,"YOU FOUND %d OF 15 JIGGIES",jiggies);
	dk_strFormat(coin_text,"%d OF 5 COINS",coins);
	dk_strFormat(cb_text,"AND %d OF 250 BANANAS",cbs);
	dl = drawTextContainer(dl, 1, 202, 175, "BANJO KONGZOOIE", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 210, 200, "BY GLORIOUSLIAR", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 91,  225, "MUSIC AND SOME ASSETS BY BISMUTH", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 212, 275, "WITH HELP FROM", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 251, 300, "BALLAAM", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 214, 325, "FAST64 DISCORD", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 141, 350, "DK64 ROMHACKING DISCORD", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 156, 400, jiggy_text, 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 238, 425, coin_text, 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 161, 450, cb_text, 0xFF, 0xFF, 0xFF, 0xFF, 0);

	dl = drawTextContainer(dl, 1, 185, 500, "THANKS FOR PLAYING", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	return dl;
}

int* displaySpiralText(int* dl) {
	dl = drawTextContainer(dl, 1, 202, 175, "MAYBE YOU SHOULD", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 223, 200, "EXPLORE MORE...", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 278, 325, "COINS", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	char coin_text[25];
	dk_strFormat(coin_text,"%d OUT OF 5",getDKCoinCount());
	dl = drawTextContainer(dl, 1, 250, 350, coin_text, 0xFF, 0xFF, 0xFF, 0xFF, 0);
	return dl;
}

int* displayCoin(int* dl) {
	dl = drawImage(dl, 119, RGBA16, 52, 52, 159, 76, 1.0f, 1.0f, 0xFF);
	return dl;
}

int* displayNoteDoorText(int* dl) {
	dl = drawTextContainer(dl, 1, 266, 375, "BANANAS", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	char banana_text[25];
	dk_strFormat(banana_text,"%d OUT OF %d",getCBCount(),NOTE_DOOR_1);
	dl = drawTextContainer(dl, 1, 248, 400, banana_text, 0xFF, 0xFF, 0xFF, 0xFF, 0);
	return dl;
}

int* displayBunch(int* dl) {
	dl = drawImage(dl, 120, RGBA16, 210, 99, 162, 86, 0.33f, 0.33f, 0xFF);
	return dl;
}

int* displayWarpText(int* dl) {
	dl = drawTextContainer(dl, 1, 160, 225, "PRESS L TO WARP TO HOUSE", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	dl = drawTextContainer(dl, 1, 240, 250, "))CREDITS))", 0xFF, 0xFF, 0xFF, 0xFF, 0);
	return dl;
}

int getJiggyCount() {
	int gb_base = 66;
	int jiggy_count = 0;
	for(int kong_number=0; kong_number<5; ++kong_number) {
		for(int level_index=0; level_index<16; level_index+=2) {
			jiggy_count += *(u16 *)(0x807FC950 + kong_number*0x5E + gb_base + level_index);
		}
	}
	return jiggy_count;
}

int getCBCount() {
	int cb_base = 10;
	int cb_count = 0;
	for(int kong_number=0; kong_number<5; ++kong_number) {
		for(int level_index=0; level_index<16; level_index+=2) {
			cb_count += *(u16 *)(0x807FC950 + kong_number*0x5E + cb_base + level_index);
		}
	}
	return cb_count;
}

int getDKCoinCount() {
	int coin_base = 6;
	int kong_number = 0;
	return *(u16 *)(0x807FC950 + kong_number*0x5E + coin_base);
}
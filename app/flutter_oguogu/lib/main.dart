import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
// import 'package:web3auth_flutter/enums.dart';
// import 'package:web3auth_flutter/input.dart';
// import 'package:web3auth_flutter/web3auth_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

import 'pages/createChallenge.dart';
import 'theme.dart';
import 'utils/mission.dart';

void main() {
  runApp(
    MaterialApp(
      initialRoute: '/',
      routes: {
        '/': (context) => LoginPage(),
        '/main': (context) => MainPage(),
      },
      theme: mainTheme,
    )
  );
}

class LoginPage extends StatefulWidget {
  LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> with WidgetsBindingObserver {
  Future<void> initWeb3Auth() async {

    late final Uri redirectUrl;

    if (Platform.isAndroid) {
      redirectUrl = Uri.parse('oguogu-app://com.katacoder.oguogu/auth');
    } else {
      // TODO: 아이폰 처리
      redirectUrl = Uri.parse('oguogu-app://auth');
    }

    // await Web3AuthFlutter.init(Web3AuthOptions(
    //   clientId: "BKFfhvts0PXY-hWj7CrryTiU_H1PBMUPql4NT7M6pMDadBCKxkLPua_mhGc3wS2IfmGyO3rHKJ25QJBe-Y_sal8",
    //   network: Network.sapphire_devnet,
    //   redirectUrl: redirectUrl,
    // ));
  }

  @override
  void initState() {
    super.initState();
    // initWeb3Auth();
    WidgetsBinding.instance.addObserver(this);
  }
  
  @override
  void dispose() {
    super.dispose();
    WidgetsBinding.instance.removeObserver(this);
  }

  @override
  void didChangeAppLifecycleState(final AppLifecycleState state) {
    // This is important to trigger the user cancellation on Android.
    // if (state == AppLifecycleState.resumed) {
    //   Web3AuthFlutter.setCustomTabsClosed();
    // }
  }  
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: TextButton(
        onPressed: () async {
          // var result = await Web3AuthFlutter.login(LoginParams(loginProvider: Provider.google,));
          // final privateKey = await Web3AuthFlutter.getPrivKey();
          // print(privateKey);

          Navigator.pushNamed(context, '/main');
        },
        child: Text("구글로 로그인하기"),
      ) ,
    );
  }
}


class MainPage extends StatefulWidget {
  MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  List<Challenge> challenges = [
    Challenge(
      title: "말해보카로 영어 공부", 
      endDate: DateTime.now().add(Duration(hours: 12)), 
      minimumProofCount: 5, 
      numProof: 4
    ),
    Challenge(
      title: "크로스핏 하러가기",
      endDate: DateTime.now().add(Duration(days: 3)), 
      minimumProofCount: 10, 
      numProof: 4
    ),
    Challenge(
      title: "하루 일기 쓰기", 
      endDate: DateTime.now().add(Duration(days: 6)), 
      minimumProofCount: 10, 
      numProof:0
    ),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void createNewChallenge(Challenge challenge) {
    setState(() {
      challenges.add(challenge);
    });
  }

  void saveData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('challenges', jsonEncode(challenges));
  }

  @override
  Widget build(BuildContext context) {
    

    return Scaffold(
      body: [
        CurrentChallegeListView(items: challenges),  
        Text("통계"),
        Text("내 정보"),
      ][_selectedIndex],


      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context, 
            MaterialPageRoute(
              builder: (context) => CreateChallengeView(createNewChallenge: createNewChallenge)
            )
          );
        },
        label: Row(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: <Widget>[
            Text('챌린지', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)), 
            SizedBox(width: 6), 
            Icon(Icons.add, size: 24)
          ],
        ),
        icon: Container(),          
      ),
      appBar: AppBar(
        actions: [
          SizedBox(width: 16),
          OutlinedButton(
            onPressed: () {},
            style: OutlinedButton.styleFrom(
              backgroundColor: culturedColor,
              side: BorderSide(color: culturedColor, width: 0),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(32.0), // 모서리를 둥글게 설정
              ),                
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min, 
              children: [
                Text('예치금: ', style: TextStyle(color: lightGrayColor, fontWeight: FontWeight.bold)),
                SizedBox(width: 4),
                Text('\$100.0', style: TextStyle(color: blackOliveColor, fontWeight: FontWeight.bold)),
              ],
            ),
          ),     
          Spacer(),
          OutlinedButton(
            onPressed: () {},
            style: OutlinedButton.styleFrom(
              elevation:10,
              backgroundColor: culturedColor,
              side: BorderSide(color: culturedColor, width: 0),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(32.0), // 모서리를 둥글게 설정
              ),                
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min, 
              children: [
                Text('필터', style: TextStyle(color: lightGrayColor, fontWeight: FontWeight.bold)),
                SizedBox(width: 4),
                Icon(Icons.filter_list, color: lightGrayColor),
              ],
            ),
          ),
          SizedBox(width: 16),
        ],
      ),      
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: culturedColor,
          border: Border(
            top: BorderSide(color: lightGrayColor, width: 1.5),
          ),
        ),
        child: BottomNavigationBar(
          iconSize: 24,
          showSelectedLabels: false,
          showUnselectedLabels: false,
          currentIndex: _selectedIndex,
          onTap: _onItemTapped,
          items: [
            BottomNavigationBarItem(
              icon: Icon(Icons.watch_later, size: 32), 
              label: '챌린지'
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.timeline, size: 32),
              label: '통계'
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person, size: 32), 
              label: '내 정보'
            ),
          ],
        ),
      ),
  );
  }
}



class CurrentChallegeListView extends StatefulWidget {
  final List<Challenge> items;
  const CurrentChallegeListView({super.key, required this.items});

  @override
  State<CurrentChallegeListView> createState() => _CurrentChallegeListViewState();
}
class _CurrentChallegeListViewState extends State<CurrentChallegeListView> {
  final ImagePicker imagePicker = ImagePicker();
  var _isImagePicked = false;

  Future<XFile?> _pickImage(int index) async {
    _isImagePicked = true;
    try {
      return await imagePicker.pickImage(source: ImageSource.gallery);
    } catch (e) {
      print(e);
    } finally {
      _isImagePicked = false;
    }
    return null;
  }
  
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: widget.items.length,
      itemBuilder: (context, index) {
        return Container(
          margin: EdgeInsets.fromLTRB(20, 12, 20, 0),
          child: OutlinedButton(
            onPressed: () async {
              if (_isImagePicked) {
                return;
              }
              await _pickImage(index);
            },
          style: OutlinedButton.styleFrom(
            backgroundColor: culturedColor,
            foregroundColor: blackOliveColor,
            side: BorderSide(color: culturedColor, width: 1),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            padding: EdgeInsets.all(16),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                widget.items[index].title, 
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)
              ),
              SizedBox(height: 8),
              Row(  
                children: [
                  Text(
                    "남은시간:",
                    style: TextStyle(fontSize: 12, color: lightGrayColor)
                  ),
                  SizedBox(width: 4),
                  Text(
                    calculateRemainTimes(widget.items[index].endDate),
                    style: TextStyle(fontSize: 12, color: lightGrayColor, fontWeight: FontWeight.bold)
                  ),
                ],
              ),
              SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text("${widget.items[index].numProof} / ${widget.items[index].minimumProofCount}", style: TextStyle(fontSize: 12, color: lightGrayColor, fontWeight: FontWeight.bold)),
                ],
              ),
              SizedBox(height: 8),
              LinearProgressIndicator(backgroundColor: Colors.white30, color: Colors.amber, value: widget.items[index].numProof / widget.items[index].minimumProofCount )
            ]
          ),
          )
        );
      },
    );
  }
}
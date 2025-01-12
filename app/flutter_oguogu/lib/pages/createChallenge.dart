import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../theme.dart';
import '../utils/mission.dart';


class CreateChallengeView extends StatefulWidget {
  final Function(Challenge) createNewChallenge;
  const CreateChallengeView({super.key, required this.createNewChallenge});

  @override
  State<CreateChallengeView> createState() => _CreateChallengeViewState();
}

class _CreateChallengeViewState extends State<CreateChallengeView> {
  final TextEditingController titleController = TextEditingController();
  final TextEditingController _dateController = TextEditingController();

  final TextEditingController minimumProofCountController = TextEditingController();
  final TextEditingController descriptionController = TextEditingController();
  
  bool _isValid = false;

  @override
  void initState() {
    super.initState();
    titleController.addListener(_updateValidation);
    _dateController.addListener(_updateValidation);
    minimumProofCountController.addListener(_updateValidation);
    descriptionController.addListener(_updateValidation);
  }


  
  void _updateValidation() {
    setState(() {
      _isValid = (
        titleController.text.isNotEmpty 
        && _dateController.text.isNotEmpty 
        && minimumProofCountController.text.isNotEmpty
        && descriptionController.text.isNotEmpty
      );
    });
  }

  _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(Duration(days: 365)),
    );
    if (picked != null) {
      setState(() {
        _dateController.text = "${picked.toLocal()}".split(' ')[0]; // 선택된 날짜를 텍스트로 변환
      });
    }
  }  

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(
        titleSpacing:0,
        title: Text(
          "New Challenge",
          style: TextStyle(
            color: blackOliveColor,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: Container(
        padding: EdgeInsets.all(32.0),
        child: Column(
          children: [
            Flexible(
              flex: 1,
              child: TextField(
                controller: titleController,
                decoration: InputDecoration(
                  labelText: "챌린지 이름",
                  floatingLabelBehavior: FloatingLabelBehavior.always,
                  labelStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                  hintText: "예) 아침 운동하러 가기",
                  hintStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 16,
                  ),
                ),
              ),
            ),
            SizedBox(height: 50.0),
                        Flexible(
              flex: 1,
              child: TextField(
                controller: _dateController,
                readOnly: true,
                onTap: () => _selectDate(context),
                decoration: InputDecoration(
                  labelText: "챌린지 종료일",
                  floatingLabelBehavior: FloatingLabelBehavior.always,
                  labelStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                  hintText: "언제까지 챌린지를 완료해야 하는지 입력해 주세요",
                  hintStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 12,
                  ),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor,
                        width: 1.0,
                      ),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor,
                        width: 1.0,
                      ),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor, // 포커스 시 경계선 색상
                        width: 2.0,
                      ),
                    )
                ),
              ),
            ),
            SizedBox(height: 50.0),
            Flexible(
              flex: 1,
              child: TextField(
                controller: minimumProofCountController,
                inputFormatters: <TextInputFormatter>[
                    FilteringTextInputFormatter.digitsOnly
                  ],
                decoration: InputDecoration(
                  labelText: "도전 횟수",
                  floatingLabelBehavior: FloatingLabelBehavior.always,
                  labelStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                  hintText: "챌린지 완료하려면 몇 번해야 하는지 입력해 주세요",
                  hintStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 12,
                  ),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor,
                        width: 1.0,
                      ),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor,
                        width: 1.0,
                      ),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor, // 포커스 시 경계선 색상
                        width: 2.0,
                      ),
                    )
                ),
              ),
            ),
            SizedBox(height: 50.0),
            Flexible(
              flex: 1,
              child: TextField(
                controller: descriptionController,
                minLines: 3,
                maxLines: 5,
                decoration: InputDecoration(
                  labelText: "챌린지 설명",
                  floatingLabelBehavior: FloatingLabelBehavior.always,
                  labelStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                  hintText: "AI가 챌린지를 확인할 수 있도록 설명해주세요\n예) 아침운동 갔다 온 후, 어플에서 체육관 입장에 대한 기록을 스크린샷해서 제출",
                  hintStyle: TextStyle(
                    color: lightGrayColor,
                    fontSize: 12,
                  ),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor,
                        width: 1.0,
                      ),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor,
                        width: 1.0,
                      ),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(16.0),
                      borderSide: BorderSide(
                        color: lightGrayColor, // 포커스 시 경계선 색상
                        width: 2.0,
                      ),
                    )
                  ),
                
              ), 
            )
          ],
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Expanded(
            flex: 1,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: FloatingActionButton.extended(
                
                backgroundColor: _isValid ? blackOliveColor : lightGrayColor,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(32.0),
                ),
                onPressed: _isValid ? () {
                  widget.createNewChallenge(Challenge(
                  title: titleController.text,
                  endDate: DateTime.parse(_dateController.text).add(Duration(days: 1)), 
                  minimumProofCount: int.parse(minimumProofCountController.text),
                  numProof: 0,
                  ));
                  Navigator.pop(context);
                } : null,
                label: Text(
                  "챌린지 만들기",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

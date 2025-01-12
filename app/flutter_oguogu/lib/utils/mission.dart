class Challenge {
  String title;
  DateTime endDate;
  int minimumProofCount;
  int numProof;

  Challenge({
    required this.title,
    required this.endDate,
    required this.minimumProofCount,
    required this.numProof,
  });
}


String calculateRemainTimes(DateTime endDate) {
  if (endDate.difference(DateTime.now()).inHours < 0) {
    return '종료';
  }
  
  if (endDate.difference(DateTime.now()).inHours < 24) {
    return '${endDate.difference(DateTime.now()).inHours}시간';
  }
  
  return '${endDate.difference(DateTime.now()).inDays}일';
}

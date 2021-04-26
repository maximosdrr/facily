import 'package:mobx/mobx.dart';

part 'index.g.dart';

class MainStore = MainStoreBase with _$MainStore;

abstract class MainStoreBase with Store {
  @observable
  int count = 0;

  @action
  increment(v) {
    count += v;
  }
}

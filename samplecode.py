import time
import random

class User:
    def __init__(self, name):
        self.name = name

    def request_taxi(self, app, origin, destination):
        print(f"[User] {self.name} -> App: 택시 호출 요청 ({origin} -> {destination})")
        app.receive_request(self, origin, destination)

    def board_taxi(self, driver):
        print(f"[User] {self.name} -> Driver: 탑승")

    def show_driver_info(self, driver):
        print(f"[App] 기사 정보: {driver.name}, 차량번호: {driver.car_number}, 도착 예상 시간: {driver.estimate_arrival()}분")

    def notify_boarding_complete(self):
        print(f"[App] 탑승 완료 상태 표시")

    def notify_in_transit(self):
        print(f"[App] 이동 중 상태 표시")

    def notify_arrival(self):
        print(f"[App] 도착지 도착 알림")


class App:
    def __init__(self, server):
        self.server = server

    def receive_request(self, user, origin, destination):
        print(f"[App] -> Server: 호출 요청 전송")
        self.server.process_request(user, origin, destination, self)

    def update_status(self, status):
        print(f"[App] 상태 업데이트: {status}")


class Server:
    def __init__(self, drivers):
        self.drivers = drivers

    def process_request(self, user, origin, destination, app):
        print(f"[Server] -> Server: 인근 기사 찾기")
        driver = random.choice(self.drivers)
        print(f"[Server] -->> App: 배차 진행 중 안내")
        if driver.accept_request():
            print(f"[Server] -->> App: 배차 완료 정보 전송")
            user.show_driver_info(driver)
            driver.move_to_user(user, origin, destination, app, self)

    def update_driver_status(self, status):
        print(f"[Server] 상태 업데이트: {status}")


class Driver:
    def __init__(self, name, car_number):
        self.name = name
        self.car_number = car_number

    def estimate_arrival(self):
        return random.randint(2, 5)

    def accept_request(self):
        print(f"[Driver] 배차 요청 수락")
        return True

    def move_to_user(self, user, origin, destination, app, server):
        print(f"[Driver] -> User: 탑승 위치로 이동")
        time.sleep(1)
        user.board_taxi(self)
        print(f"[Driver] -> App: 탑승 완료 알림")
        app.update_status("탑승 완료")
        app.server.update_driver_status("탑승 완료")
        user.notify_boarding_complete()

        self.drive_to_destination(app, user, server)

    def drive_to_destination(self, app, user, server):
        print(f"[Driver] -> Server: 도착지로 이동 중 상태 업데이트")
        server.update_driver_status("이동 중")
        print(f"[Server] -->> App: 이동 중 정보 전송")
        user.notify_in_transit()
        time.sleep(1)
        self.arrive_destination(app, user, server)

    def arrive_destination(self, app, user, server):
        print(f"[Driver] -> App: 도착지 도착 알림")
        app.update_status("도착")
        server.update_driver_status("도착")
        user.notify_arrival()


# 시뮬레이션 실행
if __name__ == "__main__":
    server = Server([
        Driver("김기사", "12가3456"),
        Driver("이기사", "78나9012")
    ])
    app = App(server)
    user = User("홍길동")
    user.request_taxi(app, "서울역", "강남역")

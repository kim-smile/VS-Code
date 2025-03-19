import tkinter as tk
import random

# 초기화
WIDTH, HEIGHT = 800, 400
PLAYER_SIZE = 50  # 플레이어 크기
OBSTACLE_SIZE = 50  # 고정된 장애물 크기
JUMP_HEIGHT = 150  # 점프 높이
GRAVITY = 2  # 중력
OBSTACLE_SPEED = 8  # 초기 장애물 속도
OBSTACLE_INTERVAL_MIN = 1000  # 최소 장애물 생성 간격 (밀리초)
OBSTACLE_INTERVAL_MAX = 1500  # 최대 장애물 생성 간격 (밀리초)

class JumpGame:
    def __init__(self, root):
        self.root = root
        self.root.title("점프 게임")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        # 게임 요소
        self.player = self.canvas.create_rectangle(50, HEIGHT - PLAYER_SIZE, 50 + PLAYER_SIZE, HEIGHT, fill="red")
        self.obstacles = []  # 여러 장애물을 관리하기 위한 리스트
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="점수: 0", font=("Arial", 16), fill="black")
        self.game_over_text = None

        # 게임 상태
        self.score = 0
        self.is_jumping = False
        self.is_game_over = False
        self.jump_speed = 0

        # 버튼
        self.restart_button = tk.Button(root, text="재시작", command=self.restart_game)
        self.restart_button.pack(side="left", padx=10)
        self.exit_button = tk.Button(root, text="종료", command=root.quit)
        self.exit_button.pack(side="right", padx=10)

        # 키 이벤트
        self.root.bind("<space>", self.jump)

        # 장애물 이동 및 생성
        self.move_obstacles()
        self.create_obstacle()

    def jump(self, event):
        if not self.is_game_over and not self.is_jumping:
            # 점프 시작
            self.is_jumping = True
            self.jump_speed = -20  # 점프 속도 증가
            self.perform_jump()

    def perform_jump(self):
        if self.is_jumping:
            self.canvas.move(self.player, 0, self.jump_speed)
            self.jump_speed += GRAVITY  # 중력에 의한 점프 속도 감소
            player_coords = self.canvas.coords(self.player)
            if player_coords[3] >= HEIGHT:
                # 착지하면 바닥에 맞추어 위치
                self.canvas.move(self.player, 0, HEIGHT - player_coords[3])
                self.is_jumping = False
            else:
                self.root.after(20, self.perform_jump)  # 점프 지속 시간 조정

    def create_obstacle(self):
        if not self.is_game_over:
            # 장애물이 1층(바닥)에서만 생성
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - OBSTACLE_SIZE  # 장애물 위치 (1층)
            obstacle = self.canvas.create_rectangle(obstacle_x, obstacle_y, obstacle_x + OBSTACLE_SIZE, obstacle_y + OBSTACLE_SIZE, fill="black")
            self.obstacles.append(obstacle)

            # 일정 시간 후 새로운 장애물 생성 (간격을 랜덤하게 설정)
            next_obstacle_interval = random.randint(OBSTACLE_INTERVAL_MIN, OBSTACLE_INTERVAL_MAX)
            self.root.after(next_obstacle_interval, self.create_obstacle)

    def move_obstacles(self):
        global OBSTACLE_SPEED, OBSTACLE_INTERVAL_MIN, OBSTACLE_INTERVAL_MAX  # 글로벌 변수 선언

        if not self.is_game_over:
            for obstacle in self.obstacles:
                self.canvas.move(obstacle, -OBSTACLE_SPEED, 0)  # 장애물 이동
                obstacle_coords = self.canvas.coords(obstacle)

                # 장애물이 화면 밖으로 나가면 제거하고 점수 증가
                if obstacle_coords[2] < 0:
                    self.canvas.delete(obstacle)
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")

                # 충돌 감지 (플레이어가 장애물 위로 넘어갈 수 있도록)
                player_coords = self.canvas.coords(self.player)
                if (obstacle_coords[0] < player_coords[2] and obstacle_coords[2] > player_coords[0] and
                        obstacle_coords[1] < player_coords[3] and obstacle_coords[3] > player_coords[1]):
                    # 플레이어가 장애물과 충돌하면 게임 종료
                    self.game_over()

            # 난이도 상승: 장애물 속도 점차적으로 증가, 생성 간격 짧아짐
            if self.score % 10 == 0 and self.score > 0:  # 점수가 10점마다 난이도 증가
                # 속도 점차적으로 증가 (매번 0.1씩만 증가)
                if OBSTACLE_SPEED < 15:  # 최대 속도 제한 (15로 설정)
                    OBSTACLE_SPEED += 0.1  # 속도 서서히 증가

                # 생성 간격 점차적으로 감소 (매번 50ms씩만 감소)
                if OBSTACLE_INTERVAL_MIN > 400:
                    OBSTACLE_INTERVAL_MIN -= 50  # 최소 생성 간격 감소
                if OBSTACLE_INTERVAL_MAX > 800:
                    OBSTACLE_INTERVAL_MAX -= 50  # 최대 생성 간격 감소

            self.root.after(30, self.move_obstacles)  # 장애물 이동 속도

    def game_over(self):
        self.is_game_over = True
        self.game_over_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"게임 오버! 최종 점수: {self.score}", font=("Arial", 24), fill="red")

    def restart_game(self):
        global OBSTACLE_SPEED, OBSTACLE_INTERVAL_MIN, OBSTACLE_INTERVAL_MAX
        OBSTACLE_SPEED = 8  # 초기 속도
        OBSTACLE_INTERVAL_MIN = 1000  # 최소 간격
        OBSTACLE_INTERVAL_MAX = 1500  # 최대 간격
        self.score = 0
        self.is_game_over = False
        self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")
        self.canvas.coords(self.player, 50, HEIGHT - PLAYER_SIZE, 50 + PLAYER_SIZE, HEIGHT)
        for obstacle in self.obstacles:
            self.canvas.delete(obstacle)
        self.obstacles.clear()
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None

        # 재시작 후 장애물 생성
        self.move_obstacles()
        self.create_obstacle()

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    game = JumpGame(root)
    root.mainloop()
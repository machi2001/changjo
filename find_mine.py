"""
tkinter를 이용한 지뢰찾기
"""
import tkinter as tk
import random


class Mine(tk.Tk):

    is_flag = False

    def __init__(self, difficulty="easy"):
        super().__init__()

        # 매트릭스 초기화
        self.row = 9
        self.column = 9
        self.matrix = [[0 for _ in range(self.row)] for _ in range(self.column)]

        # 무작위 지뢰 초기화
        self.mine_index = []
        for i in range(5):
            temp = (random.randint(0, 8), random.randint(0, 8))
            if not temp in self.mine_index:
                self.mine_index.append(temp)
        # 지뢰 주변 숫자 부여
        for mine in self.mine_index:
            r = mine[0]
            c = mine[1]
            self.matrix[mine[0]][mine[1]] = "*"
            if r - 1 >= 0:
                if c - 1 >= 0:
                    if type(self.matrix[r - 1][c - 1]) is int:
                        self.matrix[r - 1][c - 1] += 1
                if type(self.matrix[r - 1][c]) is int:
                    self.matrix[r - 1][c] += 1
                if c + 1 < 9:
                    if type(self.matrix[r - 1][c + 1]) is int:
                        self.matrix[r - 1][c + 1] += 1

            if c - 1 >= 0:
                if type(self.matrix[r][c - 1]) is int:
                    self.matrix[r][c - 1] += 1
            if c + 1 < 9:
                if type(self.matrix[r][c + 1]) is int:
                    self.matrix[r][c + 1] += 1

            if r + 1 < 9:
                if c - 1 >= 0:
                    if type(self.matrix[r + 1][c - 1]) is int:
                        self.matrix[r + 1][c - 1] += 1
                if type(self.matrix[r + 1][c]) is int:
                    self.matrix[r + 1][c] += 1
                if c + 1 < 9:
                    if type(self.matrix[r + 1][c + 1]) is int:
                        self.matrix[r + 1][c + 1] += 1

        # 매트릭스에 버튼 위젯 부여
        self.buttons = [
            [_ for _ in range(self.row)] for _ in range(self.column)
        ]  # 버튼에 접근하기 위한 버튼 리스트
        for j, r in enumerate(self.matrix):
            for i, c in enumerate(r):
                button = tk.Button(
                    master=self,
                    text=str(c),
                    width=6,
                    height=4,
                    command=lambda i=i, j=j: self.click(j, i),
                    state="normal",
                    background="white",
                    foreground="white",
                    disabledforeground="black",
                )
                button.grid(row=j, column=i)

                self.buttons[j][i] = button

        # 하단 부분 flag 버튼
        # (이 버튼 활성화 시 매트릭스 버튼을 누르면 깃발로 바뀌고 버튼이 안눌려지도록)
        self.flag_button = tk.Button(
            master=self,
            bg="white",
            fg="black",
            text="I>\n",
            command=self.change_mode,
            width=3,
            height=3,
        ).grid(row=self.row + 3, column=self.column // 2)

    # 버튼 클릭
    def click(self, j, i):
        self.buttons[j][i].config(state="disabled")
        if self.matrix[j][i] == "*":
            for j in range(self.row):
                for i in range(self.column):
                    self.buttons[j][i].config(state="disabled", background="red")
        elif self.matrix[j][i] > 0:
            self.buttons[j][i].config(state="disabled")
        else:
            # 숫자가 나올 때까지 이어져 있는 0인 부분을 다 disabled 로 만들기 이걸 어캐하지 True 인 곳에 대해서 중심을 추가 후
            # 중심이 옮겨지는 방식으로 버튼을 열기?
            center_list = []
            center_list.append((j, i))
            for center in center_list:
                check_matrix = self.check_around(center[0], center[1])
                for r, row in enumerate(check_matrix):
                    for c, col in enumerate(row):
                        if col == True:
                            if (
                                not (center[0] - 1 + r, center[1] - 1 + c)
                                in center_list
                            ):
                                center_list.append(
                                    (center[0] - 1 + r, center[1] - 1 + c)
                                )

    # 특정 칸 중심 주변 8칸 조사 후 0 에다가 이전에 disabled 된 블럭이 아니었다면 True, 아니면 False 를 가지는 3x3 matrix 를 리턴
    # 재귀적으로 구현하려 했으나 런타임 에러 발생
    def check_around(self, j, i):
        around = [[False for _ in range(3)] for _ in range(3)]

        # 중심 기준 위 3칸 체크
        if j - 1 >= 0:
            if i - 1 >= 0:
                if self.buttons[j - 1][i - 1]["state"] != "disabled":
                    if type(self.matrix[j - 1][i - 1]) is int:
                        self.buttons[j - 1][i - 1].config(state="disabled")
                        if self.matrix[j - 1][i - 1] == 0:
                            around[0][0] = True

            if self.buttons[j - 1][i]["state"] != "disabled":
                if type(self.matrix[j - 1][i]) is int:
                    self.buttons[j - 1][i].config(state="disabled")
                    if self.matrix[j - 1][i] == 0:
                        around[0][1] = True

            if i + 1 < 9:
                if self.buttons[j - 1][i + 1]["state"] != "disabled":
                    if type(self.matrix[j - 1][i + 1]) is int:
                        self.buttons[j - 1][i + 1].config(state="disabled")

                        if self.matrix[j - 1][i + 1] == 0:
                            around[0][2] = True

        # 중심기준 좌우 2칸 체크
        if i - 1 >= 0:
            if self.buttons[j][i - 1]["state"] != "disabled":
                if type(self.matrix[j][i - 1]) is int:
                    self.buttons[j][i - 1].config(state="disabled")
                    if self.matrix[j][i - 1] == 0:
                        around[1][0] = True
        if i + 1 < 9:
            if self.buttons[j][i + 1]["state"] != "disabled":
                if type(self.matrix[j][i + 1]) is int:
                    self.buttons[j][i + 1].config(state="disabled")
                    if self.matrix[j][i + 1] == 0:
                        around[1][2] = True

        # 중심기준 아래 3칸 체크
        if j + 1 < 9:
            if i - 1 >= 0:
                if self.buttons[j + 1][i - 1]["state"] != "disabled":
                    if type(self.matrix[j + 1][i - 1]) is int:
                        self.buttons[j + 1][i - 1].config(state="disabled")

                        if self.matrix[j + 1][i - 1] == 0:
                            around[2][0] = True
            if self.buttons[j + 1][i]["state"] != "disabled":
                if type(self.matrix[j + 1][i]) is int:
                    self.buttons[j + 1][i].config(state="disabled")

                    if self.matrix[j + 1][i] == 0:
                        around[2][1] = True

            if i + 1 < 9:
                if self.buttons[j + 1][i + 1]["state"] != "disabled":
                    if type(self.matrix[j + 1][i + 1]) is int:
                        self.buttons[j + 1][i + 1].config(state="disabled")

                        if self.matrix[j + 1][i + 1] == 0:
                            around[2][2] = True
        return around

    def change_mode(self):
        pass


def main():

    game = Mine()
    game.mainloop()


if __name__ == "__main__":
    main()


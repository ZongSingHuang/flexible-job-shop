import os

from addict import Dict


def decoding_fjs_data(dir_names: list[str]) -> dict:
    # 初始化
    books = Dict()

    # 歷遍數據集
    for dir_name in dir_names:
        dir_path = os.path.join(os.getcwd(), dir_name, "Text")

        # 歷遍數據
        for file in os.listdir(dir_path):
            # 檔案路徑
            file_path = os.path.join(dir_path, file)
            file_name, file_ext = os.path.splitext(file)

            # 讀取 .fjs 檔
            if file_ext == ".fjs":
                with open(file_path) as f:
                    contents = f.readlines()

                # 取得工單總數、機台總數、每道製程平均可用的機台數
                row = contents.pop(0).split()
                # total_job = int(row[0])  # 用不到
                total_machine = int(row[1])
                # avg_machine = int(row[2])  # 用不到

                # 移除最後一筆空值
                contents.pop(-1)

                # 歷遍工單
                for job, content in enumerate(contents):
                    # 正規化
                    row = [int(v) for v in content.split()]

                    # 取得該工單的製程總數
                    num_opra = row.pop(0)

                    # 歷遍製程
                    for opra in range(num_opra):
                        # 佈置該工單的製程與機台，並初始化工時
                        books[dir_name][file_name][job][opra] = Dict(
                            {machine: float("inf") for machine in range(total_machine)}
                        )

                    # 初始化當前製程道數
                    opra = 0
                    while row:
                        # 當前製程可以在幾個機台上加工
                        num_machine = row.pop(0)
                        for v in range(num_machine):
                            # 取得機台
                            machine = row.pop(0) - 1
                            # 取得該製程在機台的加工時間
                            length = row.pop(0)
                            # 新增
                            books[dir_name][file_name][job][opra][machine] = length

                        # 更新當前製程道數
                        opra += 1
    return books


if __name__ == "__main__":
    # 數據集
    dir_names = ["Barnes", "Brandimarte_Data", "Dauzere_Data"]

    # 解碼
    books = decoding_fjs_data(dir_names=dir_names)
    111

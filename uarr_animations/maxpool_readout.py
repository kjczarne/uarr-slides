from manim import *
from uarr_animations.base import SceneWithMixin

def max_pooling(input_matrix, pool_size):
    output_shape = (
        input_matrix.shape[0] // pool_size, 
        input_matrix.shape[1] // pool_size
    )
    output_matrix = np.zeros(output_shape)
    for i in range(0, input_matrix.shape[0], pool_size):
        for j in range(0, input_matrix.shape[1], pool_size):
            output_matrix[i//pool_size, j//pool_size] = np.max(
                input_matrix[i:i+pool_size, j:j+pool_size]
            )
    return output_matrix


def maxpool(scene: SceneWithMixin, window_size: int = 2):

    # Define the input matrix and calculate the output matrix using NumPy
    input_matrix = np.array([
        [1, 3, 2, 1],
        [4, 6, 5, 2],
        [7, 9, 8, 4],
        [3, 2, 4, 5]
    ])

    output_matrix = max_pooling(input_matrix, pool_size=2)

    output_matrix_unk_row = ["?" for _ in range(output_matrix.shape[1])]

    # Create input and output matrices using Matrix class
    input_matrix_mob = Matrix(input_matrix.tolist()).shift(3 * LEFT)
    output_matrix_mob = Matrix([output_matrix_unk_row for _ in range(output_matrix.shape[0])]).shift(3 * RIGHT)
    arrow = LabeledArrow(label=Text("Max Pooling", font_size=12), start=input_matrix_mob.get_right(), end=output_matrix_mob.get_left())

    # Create a 2x2 square to encompass the elements in the top-left portion of the matrix
    # Assume each cell in the matrix has approximately the same width and height
    cell_width = input_matrix_mob.get_width() / input_matrix.shape[1]
    cell_height = input_matrix_mob.get_height() / input_matrix.shape[0]

    margin_lr = -0.4
    margin_tb = -0.2

    window = Rectangle(
        width=window_size * cell_width + margin_lr,
        height=window_size * cell_height + margin_tb,
        color=RED
    )

    # Position the square to align with the top-left 2x2 elements
    top_left_cell = input_matrix_mob.get_rows()[0][0].get_center()
    window.move_to(top_left_cell + DOWN * cell_height * 0.5)
    window.shift(RIGHT * cell_width * 0.5)

    # Animation to slide the window and update the output matrix
    animations = []
    animations.append(Create(window))


    # Add elements to the scene and play the animations
    scene.add(input_matrix_mob, output_matrix_mob, arrow)
    scene.play(AnimationGroup(*animations, lag_ratio=1.5))

    def shift_window_right(window, pos):
        scene.play(window.animate.shift(pos * cell_width * RIGHT))

    def shift_window_down(window, pos):
        scene.play(window.animate.shift(pos * cell_height * DOWN))

    def shift_window_to_the_beginning(window, hops: int = 3):
        scene.play(window.animate.shift(LEFT * hops + (RIGHT * cell_width * 0.5)))

    def loop_right(row: int, call_counter: int = 0):
        for j in range(0, input_matrix.shape[1], window_size):
            shift_window_right(window, j)
            update_output_matrix(row, j, call_counter)
            call_counter += 1
        return call_counter

    # Update the output matrix as the window moves
    def update_output_matrix(i, j, u):
        max_value = output_matrix[i//window_size, j//window_size]
        cell = output_matrix_mob.get_entries()[u]
        scene.play(Transform(cell, MathTex(f"{max_value}").move_to(cell)))
        scene.play(Indicate(cell))

    call_counter = 0
    for i in range(0, input_matrix.shape[0], window_size):
        call_counter = loop_right(i, call_counter)
        # call_counter += 1
        shift_window_to_the_beginning(window)
        if i != input_matrix.shape[0] - window_size:
            shift_window_down(window, window_size)
    scene.wait(2)


def main():
    input_matrix = np.array([
        [1, 3, 2, 1],
        [4, 6, 5, 2],
        [7, 9, 8, 4],
        [3, 2, 4, 5]
    ])
    pooled = max_pooling(input_matrix, pool_size=2)
    print(pooled)


if __name__ == "__main__":
    main()

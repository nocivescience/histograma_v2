from manim import *
class ShowDistributionOfScores(Scene):
    CONFIG = {
        "axes_config": {
            "x_range":[-1,3,1.2],
            "y_range":[0,100,0.065],
            "y_axis_config": {
                "include_tip": False,
                "include_numbers":False,
            },
            'x_axis_config':{
                'include_tip':False
            }
        },
        "random_seed": 1,
    }

    def construct(self):
        # Add axes
        axes = self.get_axes()
        self.add(axes)

        # setup scores
        n_scores = 10000
        scores = np.array([self.get_random_score() for x in range(n_scores)])
        index_tracker = ValueTracker(n_scores)

        def get_index():
            value = np.clip(index_tracker.get_value(), 0, n_scores - 1)
            return int(value)

        # Setup histogram
        bars = self.get_histogram_bars(axes)
        bars.add_updater(
            lambda b: self.set_histogram_bars(
                b, scores[:get_index()], axes
            )
        )
        self.add(bars)

        # Add curr_score_arrow
        curr_score_arrow = Arrow(0.25 * UP, ORIGIN, buff=0)
        curr_score_arrow.set_stroke(WHITE, 5)
        curr_score_arrow.add_updater(
            lambda m: m.next_to(bars[scores[get_index() - 1] - 1], UP, SMALL_BUFF)
        )
        self.add(curr_score_arrow)

        # Add mean bar
        # mean_line = DashedLine(ORIGIN, 4 * UP)
        # mean_line.set_stroke(YELLOW, 2)

        # def get_mean():
        #     return np.mean(scores[:get_index()])

        # mean_line.add_updater(
        #     lambda m: m.move_to(axes.c2p(get_mean(), 0), DOWN)
        # )
        # mean_label = VGroup(
        #     Text("Mean = "),
        #     DecimalNumber(num_decimal_places=3),
        # )
        # mean_label.arrange(RIGHT)
        # mean_label.match_color(mean_line)
        # mean_label.add_updater(lambda m: m.next_to(mean_line, UP, SMALL_BUFF))
        # mean_label[1].add_updater(lambda m: m.set_value(get_mean()))

        # # Show many runs
        # index_tracker.set_value(1)
        # for value in [10, 100, 1000, 10000]:
        #     anims = [
        #         ApplyMethod(
        #             index_tracker.set_value, value,
        #             rate_func=linear,
        #             run_time=5,
        #         ),
        #     ]
        #     if value == 10:
        #         anims.append(
        #             FadeIn(
        #                 VGroup(mean_line, mean_label),
        #                 rate_func=squish_rate_func(smooth, 0.5, 1),
        #                 run_time=2,
        #             ),
        #         )
        #     self.play(*anims)
        # self.wait()

    #
    def get_axes(self):
        axes = Axes(x_range=self.CONFIG['axes_config']['x_range'], y_range=self.CONFIG['axes_config']['y_range'], y_axis_config=self.CONFIG['axes_config']['y_axis_config'])
        axes.to_corner(DL)

        axes.x_axis.add_numbers(*[range(1, 12)])
        axes.y_axis.add_numbers(
            *[range(20, 120, 20)],
            
        )
        x_label = Text("Score")
        x_label.next_to(axes.x_axis.get_right(), UR, buff=0.5)
        x_label.shift_onto_screen()
        axes.x_axis.add(x_label)

        y_label = Text("Relative proportion")
        y_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.75)
        y_label.to_edge(UP, buff=MED_SMALL_BUFF)
        axes.y_axis.add(y_label)

        return axes

    def get_histogram_bars(self, axes):
        bars = VGroup()
        for x in range(1, 10):
            bar = Rectangle(width=axes.x_axis.unit_size)
            bar.move_to(axes.c2p(x, 0), DOWN)
            bar.x = x
            bars.add(bar)
        bars.set_fill(opacity=0.7)
        bars.set_color_by_gradient(BLUE, YELLOW, RED)
        bars.set_stroke(WHITE, 1)
        return bars

    def get_relative_proportion_map(self, all_scores):
        scores = set(all_scores)
        n_scores = len(all_scores)
        return dict([
            (s, np.sum(all_scores == s) / n_scores)
            for s in set(scores)
        ])

    def set_histogram_bars(self, bars, scores, axes):
        prop_map = self.get_relative_proportion_map(scores)
        epsilon = 1e-6
        for bar in bars:
            prop = prop_map.get(bar.x, epsilon)
            bar.stretch_to_fit_height(
                prop * axes.y_axis.unit_size * 100,
                about_edge=DOWN,
            )

    def get_random_score(self):
        random_number=np.random.random()
        if random_number>.75:
            score=1
        else:
            score=2
        return score
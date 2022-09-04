from manim import *
class ShowDistributionOfScores(Scene):
    CONFIG = {
        "axis_config": {
            "x_range":[0,3,1.2],
            "y_range":[0,100,0.065],
            "y_axis_config": {
                "include_tip": False,
                "include_numbers":False,
            },
            'x_axis_config':{
                'include_tip':False,
                "include_numbers":False,
            }
        },
        "random_seed": 1,
    }

    def construct(self):
        axes = self.get_axes()
        titles=self.get_apruebo_rechazo(axes)
        self.add(axes,titles)
        n_scores = 10000
        scores = np.array([self.get_random_score() for x in range(n_scores)])
        index_tracker = ValueTracker(n_scores)

        def get_index():
            value = np.clip(index_tracker.get_value(), 0, n_scores - 1)
            return int(value)
        bars = self.get_histogram_bars(axes)
        bars.add_updater(
            lambda b: self.set_histogram_bars(
                b, scores[:get_index()], axes
            )
        )
        self.add(bars)
        index_tracker.set_value(1)
        for value in [10, 100, 1000, 10000]:
            anims = [
                ApplyMethod(
                    index_tracker.set_value, value,
                    rate_func=linear,
                    run_time=5,
                ),
            ]
            self.play(*anims)
        self.wait()
    def get_axes(self):
        axes = Axes(**self.CONFIG['axis_config'])
        axes.center()
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
    def get_apruebo_rechazo(self,axes):
        apruebo=Text('Apruebo')
        rechazo=Text('Rechazo')
        apruebo.next_to(
            axes.c2p(2,0),DOWN,buff=SMALL_BUFF
        )
        rechazo.next_to(
            axes.c2p(1,0),DOWN,buff=SMALL_BUFF
        )
        return VGroup(apruebo,rechazo)
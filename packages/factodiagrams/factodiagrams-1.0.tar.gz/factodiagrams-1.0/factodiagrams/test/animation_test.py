import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + "..") * 2)
import warnings
import factodiagrams as fd


class AnimationTest(unittest.TestCase):

    def test_generatePoints(self):
        actual = []
        for i in range(6):
            actual.append((fd.vis.points.generatePoints([2, 3])[i].x, fd.vis.points.generatePoints([2, 3])[i].y))
        expected = [(8.948255447057073e-17, 1.461361014994233), (3.298212544416459e-17, 0.538638985005767), (-1.265575763085218, -0.7306805074971161), (-0.4664750444836597, -0.2693194925028834), (1.2655757630852174,-0.7306805074971171), (0.4664750444836594, -0.2693194925028838)]
        self.assertEqual(actual,expected)
    
    def test_generate_color(self):
        actual = fd.vis.animation.Draw.generate_color(1, 0.5, 12)
        expected = (0.5, 0.125, 0.0)
        self.assertEqual(actual,expected)
    
    def test_compute_current_position(self):
        actual = (fd.vis.animation.Draw.compute_current_position(None, fd.vis.points.generatePoints([2,3])[1], fd.vis.points.generatePoints([7])[1], 60, 3).x, fd.vis.animation.Draw.compute_current_position(None, fd.vis.points.generatePoints([2,3])[1], fd.vis.points.generatePoints([7])[1], 60, 3).y)
        expected = (-0.052122098831201946, 0.5442957061292981)
        self.assertEqual(actual,expected)

    def test_Draw(self):
        actual = fd.vis.animation.Draw
        self.assertTrue(type(actual), fd.vis.animation.Draw)
    
    


if __name__ == "__main__":
    unittest.main()

import unittest
import torch
from torch import Tensor

from pietoolbelt.metrics.torch.detection import _calc_boxes_areas, _compute_boxes_iou, f_beta_score, calc_tp_fp_fn

__all__ = ['PyTorchTest']


class PyTorchTest(unittest.TestCase):
    def test_calc_boxes_areas(self):
        boxes = torch.FloatTensor([[1, 1, 2, 2], [3, 3, 5, 5], [1, 3, 2, 5], [-1, -3, 2, 5]])
        res = _calc_boxes_areas(boxes)
        self.assertIsInstance(res, Tensor)
        self.assertTrue(torch.allclose(res, torch.FloatTensor([1, 4, 2, 24])))

    def test_boxex_iou(self):
        pred = torch.FloatTensor([[0, 1, 3, 3]])
        target = torch.FloatTensor([[1, 1, 2, 2], [3, 3, 5, 5], [1, 3, 2, 5], [-1, -3, 2, 5]])
        pred_areas = _calc_boxes_areas(pred)
        target_areas = _calc_boxes_areas(target)
        res = _compute_boxes_iou(pred[0], target, pred_areas[0], target_areas)
        self.assertTrue(torch.allclose(res, torch.FloatTensor([1 / 6, 0, 0, 4 / 26])))

        pred = torch.FloatTensor([[3, 0, 5, 2], [3.5, 3.5, 5.5, 5.5]])
        target = torch.FloatTensor([[0, 0, 2, 2], [3, 3, 5, 5]])
        pred_areas = _calc_boxes_areas(pred)
        target_areas = _calc_boxes_areas(target)
        res = _compute_boxes_iou(pred[0], target, pred_areas[0], target_areas)
        self.assertTrue(torch.allclose(res, torch.FloatTensor([0, 0])))
        res = _compute_boxes_iou(pred[1], target, pred_areas[0], target_areas)
        self.assertTrue(torch.allclose(res, torch.FloatTensor([0, 2.25 / 5.75])))

    def test_tp_fp_fn(self):
        preds = torch.FloatTensor([[3, 0, 5, 2], [3.5, 3.5, 5.5, 5.5]])
        target = torch.FloatTensor([[0, 0, 2, 2], [3, 3, 5, 5]])
        tp, fp, fn = 1, 1, 1

        res = calc_tp_fp_fn(preds, target, threshold=0.1)
        self.assertEqual(res, (tp, fp, fn))

        res = calc_tp_fp_fn(preds, target, threshold=2.25 / 5.75)
        self.assertEqual(res, (tp, fp, fn))

        res = calc_tp_fp_fn(preds, target, threshold=2.25 / 5.75 + 1e-6)
        self.assertEqual(res, (0, 2, 2))

    def test_f_beta(self):
        preds = torch.FloatTensor([[[3, 0, 5, 2], [3.5, 3.5, 5.5, 5.5]]])
        target = torch.FloatTensor([[[0, 0, 2, 2], [3, 3, 5, 5]]])

        beta = 1
        tp, fp, fn = 1, 1, 1
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)

        beta_squared = beta ** 2
        expected_res = (beta_squared + 1) * (precision * recall) / (beta_squared * precision + recall + 1e-7)

        res = f_beta_score(preds, target, beta=2, thresholds=[0.1])
        self.assertAlmostEqual(res, expected_res, delta=1e-6)

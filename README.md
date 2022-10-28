# PerformanceDiagram

## 示例
```python
fig, ax = plt.subplots(dpi=123, figsize=(12, 6))
dia = PerformanceDiagram(ax, df.iloc[:, 5], df.iloc[:, 6:], bounds=[0, 1, 0, 1])
fig.legend(dia.points, [p.get_label() for p in dia.points], loc='lower center',
           ncol=7, frameon=False, bbox_to_anchor=(0.1, 0, 0.8, 0.1))
```
![image](https://user-images.githubusercontent.com/51939531/198544008-0a83a604-dfcd-4c65-b314-7f6500fc5a06.png)


`其他详细信息参考泰勒图`

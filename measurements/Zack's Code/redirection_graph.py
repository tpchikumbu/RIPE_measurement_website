import matplotlib.pyplot as plt
import json

data = []
with open('eu_cdn.txt', 'r') as file:
    for line in file:
        data.append(line)

cities = json.loads(data[0])
countries = json.loads(data[1])

sorted_cities = dict(sorted(cities.items(), key=lambda item: item[1]))
sorted_countries = dict(sorted(countries.items(), key=lambda item: item[1]))

fig, axes = plt.subplots(1, 2, figsize=(14, 8))
fig.suptitle('AWS CDN Redirections from Europe by City and Country')

axes[0].barh(list(sorted_cities.keys()), list(sorted_cities.values()), color="skyblue")
axes[0].set_title('Redirection City')
axes[0].set_xlabel('CDN Redirections')
axes[0].set_ylabel('City')

for i, (city, value) in enumerate(sorted_cities.items()):
    axes[0].text(value + 0.2, i, str(value), va='center')

axes[1].barh(list(sorted_countries.keys()), list(sorted_countries.values()), color="salmon")
axes[1].set_title('Redirection Country')
axes[1].set_xlabel('CDN Redirections')
axes[1].set_ylabel('Country')

for i, (country, value) in enumerate(sorted_countries.items()):
    axes[1].text(value + 0.2, i, str(value), va='center')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

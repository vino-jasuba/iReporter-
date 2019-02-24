const utils = {
  groupBy: (collection, key) => {
    return collection.reduce(function (accumulator, currentItem) {
      (accumulator[currentItem[key]] = accumulator[currentItem[key]] || []).push(currentItem)
      return accumulator
    }, {})
  }
}

module.exports = utils

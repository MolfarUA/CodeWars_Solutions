var User = (function () {
  ////////// Hidden //////////
  var hierarchy = [ -8,-7,-6,-5,-4,-3,-2,-1, 1, 2, 3, 4, 5, 6, 7, 8 ];
  var progress = { min: 0, max: 100 };
  var rank = { min: hierarchy[0], max: hierarchy[hierarchy.length - 1] };
  
  progress.acceleration = function (userRank, activityRank) {
    var d = rank.difference(userRank, activityRank);
    if (d === -1)       return 1;
    else if (d === 0)   return 3;
    else if (d > 0)     return 10 * d * d;
    else                return 0;
  };
  progress.update = function (user, acceleration) {
    user.progress += acceleration;
    user.progress = (user.rank === rank.max) ? progress.min : user.progress % progress.max;
  };
  rank.difference = function (userRank, activityRank) {
    return hierarchy.indexOf(activityRank) - hierarchy.indexOf(userRank);
  };
  rank.update = function (user, acceleration) {
    var d = ~~((user.progress + acceleration) / progress.max);
    var i = hierarchy.indexOf(user.rank) + d;
    if (i >= hierarchy.length) i = hierarchy.length -1;
    user.rank = hierarchy[i];
  };
  rank.valid = function (r) {
    return hierarchy.indexOf(r) > -1;
  };
  
  ////////// Exposed //////////
  var User = function () {
    this.progress = progress.min;
    this.rank = rank.min;
  };
  User.prototype.incProgress = function (activityRank) {
    if (!rank.valid(activityRank)) throw new Error("Invalid activity rank given");
    var accel = progress.acceleration(this.rank, activityRank);
    rank.update(this, accel);
    progress.update(this, accel);
  };
  return User;
}).call();
_____________________________________
class User{
  constructor(){
    this.RANK = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8];
    this.pos=0;
    this.rank = this.RANK[this.pos];
    this.progress = 0;
  }
  
  incProgress(taskRank){
    taskRank = this.RANK.indexOf(taskRank);
    if(taskRank < 0) throw ("error");
    let diff = taskRank - this.pos;
    
         if(diff ==  0) this.progress+=3;
    else if(diff >   0) this.progress += diff*diff*10;
    else if(diff == -1) this.progress += 1;
    // new rank & progress
    this.pos += Math.floor(this.progress/100);
    this.progress = this.progress%100;
    if(this.pos >= 15) {this.pos = 15; this.progress = 0;}
    this.rank = this.RANK[this.pos];
  }
  
}
_____________________________________
class User {
  constructor() {
    this.totalProgress = 0;
  }
  
  get progress() {
    return this.rank < 8 ? this.totalProgress % 100 : 0;
  }
  
  get rank() {
    let rank = Math.floor(this.totalProgress / 100) - 8;
    return rank >= 0 ? rank + 1 : rank;
  }
  
  incProgress(rank) {
    if (rank === 0 || rank < -8 || rank > 8) {
      throw new Error('Rank out of bounds');
    }
    
    if (rank > 0  && this.rank < 0) {
      rank--;
    }

    const diff = rank - this.rank;
    this.totalProgress += diff > 0 ? (10 * diff * diff) : diff < 0 ? 1 : 3;
  }
}
_____________________________________
var ranks = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8];

User = function() {
  this._progress = 0;
  
  this.incProgress = function(rank) {
    if (rank > 8) throw Error();
    if (rank == 0) throw Error();
    if (rank < -8) throw Error();
    if (rank > 0) rank--;
    var thisrank = this.rank;
    if (thisrank > 0) thisrank--;
    var cmp = rank - thisrank;
    if (cmp == 0) this._progress += 3;
    if (cmp == -1) this._progress += 1;
    if (cmp > 0) this._progress += 10 * cmp * cmp;
  }
  
  Object.defineProperty(this, "rank", { get: function () {
    return ranks[Math.min(15,Math.floor(this._progress/100))];
  }});
  
  Object.defineProperty(this, "progress", { get: function () {
    return Math.min(this._progress, 1500) % 100;
  }});
}

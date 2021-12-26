#import <Foundation/Foundation.h>

NSString *pigIt(NSString *s) {
  NSError *error = nil;
  NSRegularExpression *re = [NSRegularExpression regularExpressionWithPattern:@"([a-z])([a-z]*)" options:NSRegularExpressionCaseInsensitive error:&error];
  NSString *res = [re stringByReplacingMatchesInString:s options:0 range:NSMakeRange(0, [s length]) withTemplate:@"$2$1ay"];
  return res;
}

##########################
#import <Foundation/Foundation.h>

NSString *pigIt(NSString *s) {
  NSArray *splitArray = [ s componentsSeparatedByString:@" " ];
    
    NSMutableString *returnString = [ [ NSMutableString alloc ] init ];
    
    for ( int i = 0; i < splitArray.count; i++ )
    {
        NSString *targetString = [ splitArray objectAtIndex:i ];
        [ returnString appendString:[ NSString stringWithFormat:@"%@%@ay%@", [ targetString substringFromIndex:1 ], [ targetString substringToIndex:1 ], ( i != splitArray.count - 1 ) ? @" " : @"" ] ];
    }
    
    return returnString;
}

#################
#import <Foundation/Foundation.h>

NSString *pigIt(NSString *s) {
  NSArray *splitArray = [ s componentsSeparatedByString:@" " ];
    
    NSMutableString *returnString = [ [ NSMutableString alloc ] init ];
    
    for ( int i = 0; i < splitArray.count; i++ )
    {
        NSString *targetString = [ splitArray objectAtIndex:i ];
        [ returnString appendString:[ NSString stringWithFormat:@"%@%@ay%@", [ targetString substringFromIndex:1 ], [ targetString substringToIndex:1 ], ( i != splitArray.count - 1 ) ? @" " : @"" ] ];
    }
    
    return returnString;
}

################
#import <Foundation/Foundation.h>

NSString *pigIt(NSString *s) {
  NSError *error = nil;
  NSRegularExpression *re = [NSRegularExpression regularExpressionWithPattern:@"([a-z])([a-z]*)" options:NSRegularExpressionCaseInsensitive error:&error];
  NSString *res = [re stringByReplacingMatchesInString:s options:0 range:NSMakeRange(0, [s length]) withTemplate:@"$2$1ay"];
  return res;
}

####################
#import <Foundation/Foundation.h>
NSString *pigAWord(NSString *s) {
  return [NSString stringWithFormat:@"%@%cay", 
    [s substringWithRange:NSMakeRange(1,[s length]-1)],[s characterAtIndex:0]];
}
NSString *pigIt(NSString *s) {
  NSMutableArray *pigify = [s componentsSeparatedByString:@" "];
  for (int i=0; i<[pigify count]; ++i) {
    pigify[i] = pigAWord(pigify[i]);
  }
  return [pigify componentsJoinedByString:@" "];
}

###########################
#import <Foundation/Foundation.h>

NSString *pigIt(NSString *s) {
  NSArray<NSString *> *words = [s componentsSeparatedByString:@" "];
  NSMutableString *output = [NSMutableString stringWithCapacity:[s length]];
  NSInteger wordCount = [words count];
  [words enumerateObjectsUsingBlock:^(NSString *obj, NSUInteger idx, BOOL *stop){
        [output appendFormat:@"%@%@ay%@", [obj substringFromIndex:1], [obj substringToIndex:1], (idx < (wordCount - 1)) ? @" " : @""];
  }];
  return output;
}

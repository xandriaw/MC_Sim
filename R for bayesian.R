library(dplyr)
library(tidyr)
library(Lahman)

library(dplyr)
num_trials <- 10e6
simulations <- data_frame(
  true_average = rbeta(num_trials, 81, 219),
  hits = rbinom(num_trials, 300, true_average)
)

career <- Batting %>%
  dplyr::filter(AB > 0) %>%
  anti_join(Pitching, by = "playerID") %>%
  group_by(playerID) %>%
  summarize(H = sum(H), AB = sum(AB)) %>%
  mutate(average = H / AB)

career <- Master %>%
  tbl_df() %>%
  dplyr::select(playerID, nameFirst, nameLast) %>%
  unite(name, nameFirst, nameLast, sep = " ") %>%
  inner_join(career, by = "playerID")
# values estimated by maximum likelihood in Chapter 3

library(stats4)
library(VGAM)
career_filtered <- career %>%
  dplyr::filter(AB > 500)
# log-likelihood function
ll <- function(alpha, beta) {
  x <- career_filtered$H #x e.g. number of "heads" or "hits" in this case
  total <- career_filtered$AB #size, e.g. number of trials is the number at bats
  -sum(VGAM::dbetabinom.ab(x, total, alpha, beta, log = TRUE))
}
hist(x/total,breaks=20)
m <- mle(ll, start = list(alpha = 1, beta = 10), method = "L-BFGS-B",
         lower = c(0.0001, .1))
ab <- coef(m)
alpha0 <- ab[1]
beta0 <- ab[2]

alpha0 <- 101.4
beta0 <- 287.3
career_eb <- career %>%
  mutate(eb_estimate = (H + alpha0) / (AB + alpha0 + beta0),
         alpha1 = H + alpha0,
         beta1 = AB - H + beta0)
career_eb %>%
  dplyr::filter(name == "Hank Aaron")
#note he has alpha of about 3850 and beta of about 8881
pbeta(q=.3, shape1= 3850, shape2=8818)  #shape 1 is alpha and shape 2 is beta

xplots<- seq(0:.35,.001)
yplots<- predict(m, xplots, type="response")
pbeta



pl.beta <- function(a,b, asp = if(isLim) 1, ylim = if(isLim) c(0,1.1)) {
  if(isLim <- a == 0 || b == 0 || a == Inf || b == Inf) {
    eps <- 1e-10
    x <- c(0, eps, (1:7)/16, 1/2+c(-eps,0,eps), (9:15)/16, 1-eps, 1)
  } else {
    x <- seq(0, 1, length = 1025)
  }
  fx <- cbind(dbeta(x, a,b), pbeta(x, a,b), qbeta(x, a,b))
  f <- fx; f[fx == Inf] <- 1e100
  matplot(x, f, ylab="", type="l", ylim=ylim, asp=asp,
          main = sprintf("[dpq]beta(x, a=%g, b=%g)", a,b))
  abline(0,1,     col="gray", lty=3)
  abline(h = 0:1, col="gray", lty=3)
  legend("top", paste0(c("d","p","q"), "beta(x, a,b)"),
         col=1:3, lty=1:3, bty = "n")
  invisible(cbind(x, fx))
}

x <- seq(0, 1, length = 21)
dbeta(x, 1, 1)
pbeta(x, 1, 1)

pl.beta(3,1)

pl.beta(2, 4)
pl.beta(3, 7)
pl.beta(3, 7, asp=1)
